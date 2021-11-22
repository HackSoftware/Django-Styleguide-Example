from .base import *  # noqa

from config.env import env

DEBUG = env.bool('DJANGO_DEBUG', default=False)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

CORS_ALLOW_ALL_ORIGINS = False
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
