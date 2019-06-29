from .project import *  # noqa

# Set debug to True for development
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable caching while in development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

def show_toolbar(request):
    return True

SHOW_TOOLBAR_CALLBACK = show_toolbar

# TODO: take these keys to .secret
AWS_S3_ACCESS_KEY_ID = 'AKIAJT4AJUNRFOYF273Q'
AWS_S3_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mozio-devops.signin'

DEFAULT_ABSOLUTE_ROOT_URI = 'https://127.0.0.1:8001/'

# value of this setting will be changed in middleware!
ABSOLUTE_ROOT_URI = DEFAULT_ABSOLUTE_ROOT_URI

# Seting ``RAVEN_CONFIG`` to an empty dict disables the Raven/Sentry remote logger,
# to prevent the development environment from sending out Raven events to our main
# Sentry channel.
#
# If this is undesired either:
# - comment/delete the following line to re-enable the Raven/Sentry remote logger, or
# - configure the ``RAVEN_CONFIG`` setting to you liking, but *do not* use the staging/production Raven DSN
RAVEN_CONFIG = {}

# Make sure static files storage is set to default
STATIC_FILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # define output formats
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': (
                '%(name)s %(levelname)s %(filename)s L%(lineno)s: '
                '%(message)s')
        },
    },
    'handlers': {
        # console output
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',  # switch to DEBUG to show actual SQL
        }
    },
    # root logger
    # non handled logs will propagate to the root logger
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    }
}

PIPELINE['PIPELINE_ENABLED'] = False
