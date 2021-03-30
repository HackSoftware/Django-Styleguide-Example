from .env_reader import env


"""
Do read:

    1. https://docs.djangoproject.com/en/3.1/ref/settings/#sessions
    2. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
"""
SESSION_COOKIE_AGE = env.int('DJANGO_SESSION_COOKIE_AGE', default=1209600)  # Default - 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = env.bool('DJANGO_SESSION_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_NAME = env('DJANGO_SESSION_COOKIE_NAME', default='sessionid')
SESSION_COOKIE_SAMESITE = env('DJANGO_SESSION_COOKIE_SAMESITE', default=False)
SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', default=False)

CSRF_USE_SESSIONS = env.bool('DJANGO_CSRF_USE_SESSIONS', default=True)
