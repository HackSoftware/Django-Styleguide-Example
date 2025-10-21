# https://mattsegal.dev/django-gunicorn-nginx-logging.html
# https://albersdevelopment.net/2019/08/15/using-structlog-with-gunicorn/

import logging
import logging.config
import re

import structlog


def combined_logformat(logger, name, event_dict):
    if event_dict.get("logger") == "gunicorn.access":
        message = event_dict["event"]

        parts = [
            r"(?P<host>\S+)",  # host %h
            r"\S+",  # indent %l (unused)
            r"(?P<user>\S+)",  # user %u
            r"\[(?P<time>.+)\]",  # time %t
            r'"(?P<request>.+)"',  # request "%r"
            r"(?P<status>[0-9]+)",  # status %>s
            r"(?P<size>\S+)",  # size %b (careful, can be '-')
            r'"(?P<referer>.*)"',  # referer "%{Referer}i"
            r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
        ]
        pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")
        m = pattern.match(message)
        res = m.groupdict()

        if res["user"] == "-":
            res["user"] = None

        res["status"] = int(res["status"])

        if res["size"] == "-":
            res["size"] = 0
        else:
            res["size"] = int(res["size"])

        if res["referer"] == "-":
            res["referer"] = None

        event_dict.update(res)

    return event_dict


timestamper = structlog.processors.TimeStamper(fmt="iso", utc=True)
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    structlog.stdlib.add_logger_name,
    timestamper,
    combined_logformat,
]

CONFIG_DEFAULTS = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["default"]},
    "loggers": {
        "gunicorn.error": {"level": "INFO", "handlers": ["default"], "propagate": False, "qualname": "gunicorn.error"},
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
        "django_structlog": {
            "level": "INFO",
            "handlers": [],
            "propagate": False,
        },
    },
    "handlers": {
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
    },
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        }
    },
}

logging.config.dictConfig(CONFIG_DEFAULTS)
