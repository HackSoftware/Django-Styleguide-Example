import logging

import structlog


class IgnoreFilter(logging.Filter):
    def filter(self, record):
        return False


class LoggersSetup:
    """
    We use a class, just for namespacing convenience.
    """

    @staticmethod
    def setup_settings(INSTALLED_APPS, MIDDLEWARE, middleware_position=None):
        INSTALLED_APPS = INSTALLED_APPS + ["django_structlog"]

        django_structlog_middleware = "django_structlog.middlewares.RequestMiddleware"

        if middleware_position is None:
            MIDDLEWARE = MIDDLEWARE + [django_structlog_middleware]
        else:
            # Grab a new copy of the list, since insert mutates the internal structure
            _middleware = MIDDLEWARE[::]
            _middleware.insert(middleware_position, django_structlog_middleware)

            MIDDLEWARE = _middleware

        return INSTALLED_APPS, MIDDLEWARE

    @staticmethod
    def setup_structlog():
        from config.settings.loggers.settings import LOGGING_FORMAT, LoggingFormat

        logging_format = LOGGING_FORMAT

        extra_processors = []

        if logging_format == LoggingFormat.DEV:
            extra_processors = [
                structlog.processors.format_exc_info,
            ]

        if logging_format in [LoggingFormat.JSON, LoggingFormat.LOGFMT]:
            dict_tracebacks = structlog.processors.ExceptionRenderer(
                structlog.processors.ExceptionDictTransformer(show_locals=False)
            )
            extra_processors = [
                dict_tracebacks,
            ]

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                *extra_processors,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.CallsiteParameterAdder(
                    {
                        structlog.processors.CallsiteParameter.FILENAME,
                        structlog.processors.CallsiteParameter.FUNC_NAME,
                        structlog.processors.CallsiteParameter.LINENO,
                    }
                ),
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    @staticmethod
    def setup_logging():
        from config.settings.loggers.settings import LOGGING_FORMAT, LoggingFormat

        logging_format = LOGGING_FORMAT
        formatter = "dev"

        if logging_format == LoggingFormat.DEV:
            formatter = "dev"

        if logging_format == LoggingFormat.JSON:
            formatter = "json"

        if logging_format == LoggingFormat.LOGFMT:
            formatter = "logfmt"

        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "dev": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(),
                },
                "logfmt": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.LogfmtRenderer(),
                },
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
            },
            "filters": {
                "ignore": {
                    "()": "config.settings.loggers.setup.IgnoreFilter",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": formatter,
                }
            },
            "loggers": {
                # We want to get rid of the runserver logs
                "django.server": {"propagate": False, "handlers": ["console"], "filters": ["ignore"]},
                # We want to get rid of the logs for 4XX and 5XX
                "django.request": {"propagate": False, "handlers": ["console"], "filters": ["ignore"]},
                "django_structlog": {
                    "handlers": ["console"],
                    "level": "INFO",
                },
                "celery": {
                    "handlers": ["console"],
                    "level": "INFO",
                },
                "styleguide_example": {
                    "handlers": ["console"],
                    "level": "INFO",
                },
            },
        }
