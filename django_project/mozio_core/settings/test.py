from .project import *  # noqa

# http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += (
    'django_nose',  # don't remove this comma
)

DEBUG = True
PIPELINE['PIPELINE_ENABLED'] = False
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

NOSE_ARGS = (
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=xmlrunner/html',
    '--cover-inclusive',
    # '--cover-package=django_app',
    '--nocapture',
    '--nologcapture'
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'

LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'nullhandler': {
            'class': 'logging.NullHandler',
        },
    },
    # default root logger
    'root': {
        'level': 'DEBUG',
        'handlers': ['nullhandler'],
    }
}


class MigrationDisabler:
    """
    Disable all migrations in all apps when running tests.

    Django's test runner will instead create the needed tables in sqlite
    using the current model configurations at runtime.
    """

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        pass


def show_toolbar(request):
    return True

MIGRATION_MODULES = MigrationDisabler()

# CELERY_ALWAYS_EAGER = True

SHOW_TOOLBAR_CALLBACK = show_toolbar

AWS_S3_ACCESS_KEY_ID = 'AKIAJT4AJUNRFOYF273Q'
AWS_S3_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mozio-devops.signin'

DEFAULT_ABSOLUTE_ROOT_URI = 'https://127.0.0.1:8001/'

# value of this setting will be changed in middleware!
ABSOLUTE_ROOT_URI = DEFAULT_ABSOLUTE_ROOT_URI
