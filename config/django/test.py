import os

# This is extremely "eye-poking",
# but we need it, if we want to ignore the debug toolbar in tests
# This is needed because of the way we setup Django Debug Toolbar.
# Since we import base settings, the entire setup will be done, before we have any chance to change it.
# A different way of approaching this would be to have a separate set of env variables for tests.
os.environ.setdefault("DEBUG_TOOLBAR_ENABLED", "False")

from .base import *  # noqa

# Based on https://www.hacksoft.io/blog/optimize-django-build-to-run-faster-on-github-actions

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CELERY_BROKER_BACKEND = "memory"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
