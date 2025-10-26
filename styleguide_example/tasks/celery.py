from __future__ import absolute_import, unicode_literals

import logging
import os

import structlog
from celery import Celery
from celery.signals import setup_logging
from django.dispatch import receiver
from django_structlog.celery import signals
from django_structlog.celery.steps import DjangoStructLogInitStep

from config.settings.loggers.setup import LoggersSetup

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.base")

app = Celery("styleguide_example")
app.steps["worker"].add(DjangoStructLogInitStep)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # pragma: no cover
    LoggersSetup.setup_structlog()
    logging.config.dictConfig(LoggersSetup.setup_logging())


@receiver(signals.bind_extra_task_metadata)
def receiver_bind_extra_request_metadata(sender, signal, task=None, logger=None, **kwargs):
    # We want to add the task name to the task_succeeded event
    if task is not None:
        structlog.contextvars.bind_contextvars(task=task.name)
