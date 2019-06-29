# coding=utf-8
"""
mozio_core.settings.contrib
"""
from .base import *  # noqa
import os
from datetime import timedelta

import logging
import raven

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that', 'to',
)

# STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# STATICFILES_FINDERS += (
#     'pipeline.finders.PipelineFinder',
# )

# Django-allauth related settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Django grappelli need to be added before django.contrib.admin
INSTALLED_APPS = (
    'grappelli',
    'fancy_cronfield',
    'widget_tweaks',
    'django_celery_beat',
    'django_celery_results',
) + INSTALLED_APPS

# Grapelli settings
GRAPPELLI_ADMIN_TITLE = 'mozio Admin Page'

INSTALLED_APPS += (
    'easyaudit',
    'celery',
    # 'pipeline',
    # 'haystack',
    'raven.contrib.django.raven_compat',
    'storages',
    'django_summernote',
    'mathfilters',
    'online_users',
    'rest_framework',
    'rest_framework.authtoken', # for token auth
)

# MIDDLEWARE = (
#     'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
# ) + MIDDLEWARE

MIDDLEWARE += (
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'online_users.middleware.OnlineNowMiddleware',
)

# Defines whether to log model related events,
# such as when an object is created, updated, or deleted
DJANGO_EASY_AUDIT_WATCH_MODEL_EVENTS = True

# Defines whether to log user authentication events,
# such as logins, logouts and failed logins.
DJANGO_EASY_AUDIT_WATCH_AUTH_EVENTS = True

# Defines whether to log URL requests made to the project
DJANGO_EASY_AUDIT_WATCH_REQUEST_EVENTS = True

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'SCOPE': ['user:email', 'public_repo', 'read:org']
    }
}



# auth
LOGIN_URL = 'auth_login'
LOGIN_REDIRECT_URL = 'dashboard'

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
REGISTRATION_SALT = '99!@ddsa?Q@3DSDDDsaazashgie#@'

# django-reset-password
PASSWORD_RESET_TIMEOUT_DAYS = 1

CELERY_BROKER_POOL_LIMIT = 500
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_MAX_TASKS_PER_CHILD = 100
CELERY_ACKS_LATE = False
CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_COMPRESSION = 'gzip'
CELERY_BROKER_HEARTBEAT = 0

BROKER_URL = 'amqp://rabbit:rabbit_test_password@%s:5672//' % os.environ['RABBITMQ_HOST']
# CELERY_BROKER_URL = os.environ.get['BROKER_URL']
# CELERY_RESULT_BACKEND = os.environ.get['CELERY_BROKER_URL']

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel',
)

if 'INTERNAL_IPS' in os.environ:
    INTERNAL_IPS = os.environ.get('INTERNAL_IPS')
else:
    INTERNAL_IPS = ['109.97.41.76', '127.0.0.1', '83.103.233.127']

# upload
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)


# Google API key
# TODO: Take this key to .secret file for security.
GOOGLE_API_KEY = 'AIzaSyBAQqr9-k6dYvlLwbax6NvhRH-Y0fzeZ8Q'

if 'BROADCAST_REQUEST_BATCH_SIZE' in os.environ:
    BROADCAST_REQUEST_BATCH_SIZE = os.environ.get('BROADCAST_REQUEST_BATCH_SIZE')
else:
    BROADCAST_REQUEST_BATCH_SIZE = 250

if BROADCAST_REQUEST_BATCH_SIZE > 500:
    BROADCAST_REQUEST_BATCH_SIZE = 500

# Raven
RAVEN_DSN = os.environ.get('RAVEN_DSN')
RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
    'string_max_length': 10000,
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    'CELERY_LOGLEVEL': logging.INFO,
} if RAVEN_DSN else {
}

# AWS Settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_ACCESS_KEY_ID = ''
AWS_S3_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

# the next monkey patch is necessary if you use dots in the bucket name
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

SUMMERNOTE_CONFIG = {
    'width': '100%',
    'height': '250',
    'lazy': True,
}

# Django Rest Framework JWT configurations

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440), # valid for 24 hours
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
