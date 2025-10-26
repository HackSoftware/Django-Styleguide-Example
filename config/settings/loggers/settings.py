import logging
from enum import Enum

from config.env import env, env_to_enum


class LoggingFormat(Enum):
    DEV = "dev"
    JSON = "json"
    LOGFMT = "logfmt"


LOGGING_FORMAT = env_to_enum(LoggingFormat, env("LOGGING_FORMAT", default=LoggingFormat.DEV.value))

DJANGO_STRUCTLOG_STATUS_4XX_LOG_LEVEL = logging.INFO
DJANGO_STRUCTLOG_CELERY_ENABLED = True
