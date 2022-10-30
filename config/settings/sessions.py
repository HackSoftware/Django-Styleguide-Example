from config.env import env

"""
Do read:

    1. https://docs.djangoproject.com/en/3.1/ref/settings/#sessions
    2. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
"""
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", default=1209600)  # Default - 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = env.bool("SESSION_COOKIE_HTTPONLY", default=True)
SESSION_COOKIE_NAME = env("SESSION_COOKIE_NAME", default="sessionid")
SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="Lax")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)

CSRF_USE_SESSIONS = env.bool("CSRF_USE_SESSIONS", default=True)
