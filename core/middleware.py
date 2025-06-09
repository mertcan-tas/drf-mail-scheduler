import logging
import json
import uuid
from django.utils.deprecation import MiddlewareMixin

api_logger = logging.getLogger('api_logs')

class LoggingMiddleware(MiddlewareMixin):
    
    LOGGING_CONFIG = {
        '/api/auth/login/': {
            'POST': {
                'log_request': True,
                'log_response': True,
                'hide_request': True,
                'hide_response': True,
                'tag': 'auth:login',
                'category': 'authentication'
            },
        }, 
    }
    
    def process_request(self, request):
        config = self._get_path_config(request)
        if not config:
            return None
        
        if not config.get('log_request', False):
            return None
        
        request.log_id = str(uuid.uuid4())
        
        request.log_tag = config.get('tag')
        request.log_category = config.get('category')
        
        self._log_request(request, config)
        
        return None
    
    def process_response(self, request, response):
        config = self._get_path_config(request)
        if not config:
            return response
        
        if not config.get('log_response', False):
            return response
        
        self._log_response(request, response, config)
        
        return response
    
    def process_exception(self, request, exception):
        config = self._get_path_config(request)
        if not config:
            return None
        
        self._log_exception(request, exception)
        
        return None
    
    def _get_path_config(self, request):
        path = request.path
        method = request.method
        
        if path in self.LOGGING_CONFIG:
            path_config = self.LOGGING_CONFIG[path]
            if method in path_config:
                return path_config[method]
        
        return None
    
    def _log_request(self, request, config):
        try:
            request_data = None
            if not config.get('hide_request', False):
                request_data = self._extract_request_data(request)
            
            log_data = {
                'request_id': getattr(request, 'log_id', ''),
                'ip_address': self._get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'request_method': request.method,
                'request_path': request.path,
                'request_data': request_data,
                'tag': config.get('tag'),
                'category': config.get('category'),
                'action_type': 'request'
            }
            
            api_logger.info(
                f"API Request: {request.method} {request.path} - [{config.get('tag')}]",
                extra=log_data
            )
                
        except Exception as e:
            logging.error(f"Request logging error: {e}")
    
    def _log_response(self, request, response, config):
        try:
            response_data = None
            if not config.get('hide_response', False):
                response_data = self._extract_response_data(response)
            
            log_data = {
                'request_id': getattr(request, 'log_id', ''),
                'ip_address': self._get_client_ip(request),
                'request_method': request.method,
                'request_path': request.path,
                'response_status': response.status_code,
                'response_data': response_data,
                'tag': config.get('tag'),
                'category': config.get('category'),
                'action_type': 'response',
                'success': response.status_code < 400
            }
            
            log_level = self._get_log_level(response.status_code)
            
            getattr(api_logger, log_level)(
                f"API Response: {request.method} {request.path} - {response.status_code} - [{config.get('tag')}]",
                extra=log_data
            )
                
        except Exception as e:
            logging.error(f"Response logging error: {e}")
    
    def _log_exception(self, request, exception):
        try:
            config = self._get_path_config(request)
            if not config:
                return
            
            log_data = {
                'request_id': getattr(request, 'log_id', ''),
                'ip_address': self._get_client_ip(request),
                'request_method': request.method,
                'request_path': request.path,
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'tag': config.get('tag'),
                'category': config.get('category'),
                'action_type': 'exception',
                'success': False
            }
            
            api_logger.error(
                f"API Exception: {request.method} {request.path} - {str(exception)} - [{log_data['tag']}]",
                extra=log_data,
                exc_info=True
            )
                
        except Exception as e:
            logging.error(f"Exception logging error: {e}")
    
    def _extract_request_data(self, request):
        try:
            if (hasattr(request, 'content_type') and 
                request.content_type == 'application/json' and 
                hasattr(request, 'body')):
                return json.loads(request.body.decode('utf-8'))
            
            elif request.method == 'POST' and hasattr(request, 'POST'):
                return dict(request.POST)
            
            elif request.method == 'GET' and hasattr(request, 'GET'):
                return dict(request.GET)
            
        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            pass
        
        return None
    
    def _extract_response_data(self, response):
        try:
            content_type = response.get('Content-Type', '')
            if (content_type.startswith('application/json') and 
                hasattr(response, 'content')):
                
                content = response.content.decode('utf-8')
                if len(content) < 10000:
                    return json.loads(content)
                else:
                    return {'_message': 'Response too large to log'}

        except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
            pass
        
        return None
    
    def _get_log_level(self, status_code):
        if status_code >= 500:
            return 'error'
        elif status_code >= 400:
            return 'warning'
        else:
            return 'info'
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        if x_real_ip:
            return x_real_ip.strip()
        
        return request.META.get('REMOTE_ADDR', 'unknown')