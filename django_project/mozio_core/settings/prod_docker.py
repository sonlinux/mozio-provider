
"""Configuration for production server"""
# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os

DEBUG = True

ALLOWED_HOSTS = [
    '*',
    'localhost:9000',
    '127.0.0.1',
    ]

ADMINS = (
    ('Alison Mukoma', 'mukomalison@gmail.com'),
)


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}
# See fig.yml file for postfix container definition
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
DEFAULT_DOMAIN = 'mozio.com'
DEFAULT_FROM_EMAIL = 'support@mozio.com'
DEFAULT_FROM_NAME = 'mozio Support'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# SMTP authentication information for EMAIL_HOST.
# See docker-compose.yml for where these are defined
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = 'docker'

EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[mozio Support]'
