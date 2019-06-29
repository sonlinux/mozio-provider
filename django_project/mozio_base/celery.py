from __future__ import absolute_import, unicode_literals

import logging
import os

import celery
from celery.result import AsyncResult

# AsyncResult objects have a memory leak in them in Celery 4.2.1.
# See https://github.com/celery/celery/pull/4839/
delattr(AsyncResult, '__del__')

import raven
from raven.contrib.celery import register_signal, register_logger_signal


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adk.settings')


app = celery.Celery('adk')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_raven_logging(sender, **kwargs):
    # TODO: 2018-06-18 @petar.maric: Once https://gitlab.com/mozio/pyadk/issues/63
    # is resolved use ``if not sender.conf.RAVEN_ENABLED:`` instead
    # TODO: 2018-08-01 @dima: if `RAVEN_DSN` setting is None, then `RAVEN_CONFIG`
    # will be an empty dict and `client` will become kind of "Nullable Object"
    # (i.e. you can leave all calls of client methods like `client.captureMessage()`
    # and it will work just fine even without any specified DSN)

    client = raven.Client(**sender.conf.RAVEN_CONFIG)

    # register a custom filter to filter out duplicate logs
    register_logger_signal(client, loglevel=logging.ERROR)
    # hook into the Celery error handler
    register_signal(client)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
