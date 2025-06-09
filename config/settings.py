from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
from pymongo import MongoClient
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_rq',
    'drf_spectacular',
]

PROJECT_APPS = [
    'core',
    'app',
]

INSTALLED_APPS += PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.middleware.LoggingMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    },
}

MONGO_HOST = config('MONGO_HOST', default="localhost", cast=str)
MONGO_PORT = config('MONGO_PORT', default=27017, cast=int)
MONGO_DB_NAME = config('MONGO_DB_NAME', default="logs", cast=str)
MONGO_USERNAME = config('MONGO_ROOT_USERNAME', default="mongo", cast=str)
MONGO_PASSWORD = config('MONGO_ROOT_PASSWORD', default="password", cast=str)

MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://:{config('REDIS_PASSWORD')}@{config('REDIS_HOST')}/{config('REDIS_DB')}',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 200,
            },
            "SOCKET_TIMEOUT": 1.5,
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "COMPRESS_LEVEL": 4,
            "COMPRESS_MIN_LENGTH": 1024,
            "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",
            "HEALTH_CHECK_INTERVAL": 30,
            "PERSISTENT": True,
        },
        "KEY_PREFIX": "app",
        "VERSION": 1
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f'redis://:{config('REDIS_PASSWORD')}@{config('REDIS_HOST')}/{config('REDIS_DB')}'],
        },
    },
}

RQ_QUEUES = {
    'default': {
        'HOST': config('REDIS_HOST'),
        'PORT': 6379,
        'DB': config('REDIS_DB'),
        'PASSWORD': config('REDIS_PASSWORD'),
        'DEFAULT_TIMEOUT': 360,
    },
}


TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = config('EMAIL_BACKEND', default="django.core.mail.backends.smtp.EmailBackend", cast=str)
EMAIL_HOST = config('EMAIL_HOST', default="localhost", cast=str)   
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)             
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)       
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)        
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default="noreply@app.com", cast=str)           
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default="", cast=str)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),

    'ROTATE_REFRESH_TOKENS': True, 
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True, 

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DRF Mail Scheduler',
    'DESCRIPTION': 'DRF Mail Scheduler is a robust API service built with Django REST Framework and Django Q, designed to schedule and send emails asynchronously. Ideal for applications requiring delayed or periodic email delivery such as reminders, notifications, and newsletters.',
    'VERSION': '1.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000", 
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control', 
    'x-forwarded-for',  
    'x-forwarded-proto',  
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 
CSRF_COOKIE_HTTPONLY = False  
CSRF_COOKIE_SECURE = False   
SESSION_COOKIE_SECURE = False

CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_AGE = 3600

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'mongodb': {
            'level': 'DEBUG',
            'class': 'core.logging.AsyncMongoDBHandler',  
            'db_name': MONGO_DB_NAME,
            'batch_size': 10,
            'flush_interval': 2,   
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': [],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mongodb', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'api_logs': {
            'handlers': ['mongodb', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}