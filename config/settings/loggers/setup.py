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
                structlog.processors.format_exc_info,
                # structlog.processors.dict_tracebacks,
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
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
                "plain_console": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(),
                },
            },
            "filters": {
                "ignore": {
                    "()": "config.settings.loggers.setup.IgnoreFilter",
                },
            },
            "handlers": {
                # Important notes regarding handlers.
                #
                # 1. Make sure you use handlers adapted for your project.
                # These handlers configurations are only examples for this library.
                # See python's logging.handlers: https://docs.python.org/3/library/logging.handlers.html
                #
                # 2. You might also want to use different logging configurations depending of the environment.
                # Different files (local.py, tests.py, production.py, ci.py, etc.) or only conditions.
                # See https://docs.djangoproject.com/en/dev/topics/settings/#designating-the-settings
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "plain_console",
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
