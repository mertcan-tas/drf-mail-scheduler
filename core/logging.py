import logging
import json
from pymongo import MongoClient
from django.conf import settings
from django.utils import timezone
import threading
from pymongo.operations import InsertOne
import traceback

class AsyncMongoDBHandler(logging.Handler):
    def __init__(self, db_name, batch_size=100, flush_interval=5):
        super().__init__()
        self.db_name = db_name
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.client = None
        self.db = None
        self.log_queue = []
        self.last_flush = timezone.now()
        self.indexes_created = set()
        self._lock = threading.Lock()
        
        self.debug_mode = getattr(settings, 'DEBUG', False)
        
        self.connect()
        
        self._start_flush_timer()
    
    def connect(self):
        try:
            if self.client is None:
                mongo_uri = getattr(settings, 'MONGO_URI', None)
                if not mongo_uri:
                    return False
                
                self.client = MongoClient(
                    mongo_uri,
                    maxPoolSize=50,
                    minPoolSize=10,
                    maxIdleTimeMS=30000,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    retryWrites=True,
                    retryReads=True,
                    w='majority',
                    readPreference='secondaryPreferred'
                )
                
                self.db = self.client[self.db_name]
                
                self.client.server_info()
                return True
                
        except Exception as e:
            self.client = None
            self.db = None
            return False
    
    def _start_flush_timer(self):
        def flush_timer():
            try:
                while True:
                    import time
                    time.sleep(self.flush_interval)
                    with self._lock:
                        if self.log_queue:
                            self._flush_logs()
            except Exception as e:
                pass
        
        timer_thread = threading.Thread(target=flush_timer, daemon=True)
        timer_thread.start()
    
    def emit(self, record):
        try:
            if self.client is None:
                if not self.connect():
                    return
            
            with self._lock:
                log_entry = {
                    'timestamp': timezone.now(),
                    'logger_name': record.name,
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': getattr(record, 'module', ''),
                    'function': getattr(record, 'funcName', ''),
                    'line': getattr(record, 'lineno', 0),
                }
                
                safe_attributes = [
                    'request_id', 'ip_address', 'user_agent',
                    'request_method', 'request_path', 'response_status', 'request_data', 
                    'response_data', 'tag', 'category', 'action_type', 'success'
                ]
                
                for attr in safe_attributes:
                    if hasattr(record, attr):
                        value = getattr(record, attr)
                        if value is not None:
                            log_entry[attr] = value
                
                if record.exc_info:
                    log_entry['exception'] = self.format(record)
                
                self._add_tag_metadata(log_entry)
                
                collection_name = self._get_collection_name(record.name, record.levelname, log_entry.get('tag'))
                log_entry['_collection'] = collection_name
                
                self.log_queue.append(log_entry)
                
                if len(self.log_queue) >= self.batch_size:
                    self._flush_logs()
            
        except Exception as e:
            pass
    
    def _add_tag_metadata(self, log_entry):
        tag = log_entry.get('tag')
        category = log_entry.get('category')
        
        if tag:
            if ':' in tag:
                main_tag, sub_tag = tag.split(':', 1)
                log_entry['main_tag'] = main_tag
                log_entry['sub_tag'] = sub_tag
            else:
                log_entry['main_tag'] = tag
                log_entry['sub_tag'] = None
        
        if category:
            priority_mapping = {
                'authentication': 'high',
                'profile': 'medium',
                'organization': 'medium',
                'error': 'critical'
            }
            log_entry['priority'] = priority_mapping.get(category, 'low')
        
        if log_entry.get('level') == 'ERROR' or log_entry.get('success') is False:
            log_entry['requires_alert'] = True
        else:
            log_entry['requires_alert'] = False
    
    def _flush_logs(self):
        if not self.log_queue:
            return
        
        try:
            if self.client is None:
                if not self.connect():
                    self.log_queue.clear()
                    return
            
            collections_data = {}
            for log_entry in self.log_queue:
                collection_name = log_entry.pop('_collection')
                if collection_name not in collections_data:
                    collections_data[collection_name] = []
                collections_data[collection_name].append(log_entry)
            
            for collection_name, logs in collections_data.items():
                try:
                    collection = self.db[collection_name]
                    
                    if collection_name not in self.indexes_created:
                        self._ensure_indexes(collection_name)
                        self.indexes_created.add(collection_name)
                    
                    if len(logs) == 1:
                        result = collection.insert_one(logs[0])
                    else:
                        operations = [InsertOne(doc) for doc in logs]
                        result = collection.bulk_write(operations, ordered=False)
                    
                except Exception as e:
                    pass
            
            queue_size = len(self.log_queue)
            self.log_queue.clear()
            self.last_flush = timezone.now()
            
        except Exception as e:
            self.log_queue.clear()
            self.client = None
            self.db = None
    
    def _ensure_indexes(self, collection_name):
        try:
            collection = self.db[collection_name]
            
            collection.create_index("timestamp")
            collection.create_index("tag")
            collection.create_index("category")
            collection.create_index("main_tag")
            collection.create_index("priority")
            collection.create_index("requires_alert")
            
            collection.create_index([("timestamp", -1), ("tag", 1)])
            collection.create_index([("category", 1), ("timestamp", -1)])
            collection.create_index([("main_tag", 1), ("sub_tag", 1)])
            collection.create_index([("priority", 1), ("timestamp", -1)])
            collection.create_index([("requires_alert", 1), ("timestamp", -1)])
            
            if collection_name == 'api_logs':
                collection.create_index("request_id")
                collection.create_index("request_path")
                collection.create_index("response_status")
                collection.create_index([("request_path", 1), ("timestamp", -1)])
                collection.create_index([("response_status", 1), ("timestamp", -1)])
                collection.create_index([("tag", 1), ("response_status", 1)])
            
            elif collection_name == 'error_logs':
                collection.create_index("level")
                collection.create_index([("level", 1), ("timestamp", -1)])
                collection.create_index([("request_path", 1), ("level", 1)])
                collection.create_index([("tag", 1), ("level", 1)])
            
            collection.create_index([("main_tag", 1), ("timestamp", -1)])
            collection.create_index([("category", 1), ("main_tag", 1)])
            
        except Exception as e:
            pass
    
    def _get_collection_name(self, logger_name, level, tag=None):
        if tag:
            if tag.startswith('auth:'):
                return 'api_logs'
            elif tag.startswith('profile:') or tag.startswith('organization:'):
                return 'api_logs'
            elif 'error' in tag:
                return 'error_logs'
        
        if 'django.request' in logger_name:
            return 'django_request_logs'
        elif 'api_logs' in logger_name:
            return 'api_logs'
        elif level == 'ERROR':
            return 'error_logs'
        else:
            return 'system_logs'
    
    def close(self):
        try:
            with self._lock:
                if self.log_queue:
                    self._flush_logs()
        except Exception as e:
            pass
        finally:
            if self.client:
                try:
                    self.client.close()
                except:
                    pass
            super().close()