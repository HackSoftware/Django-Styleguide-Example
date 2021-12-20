import datetime

from config.env import env

# For more settings
# Read everything from here - https://styria-digital.github.io/django-rest-framework-jwt/#additional-settings

# Default to 7 days
JWT_EXPIRATION_DELTA_SECONDS = env("JWT_EXPIRATION_DELTA_SECONDS", default=60 * 60 * 24 * 7)
JWT_AUTH_COOKIE = env("JWT_AUTH_COOKIE", default="jwt")
JWT_AUTH_COOKIE_SAMESITE = env("JWT_AUTH_COOKIE_SAMESITE", default="Lax")
JWT_AUTH_HEADER_PREFIX = env("JWT_AUTH_HEADER_PREFIX", default="Bearer")


JWT_AUTH = {
    "JWT_GET_USER_SECRET_KEY": "styleguide_example.authentication.services.auth_user_get_jwt_secret_key",
    "JWT_RESPONSE_PAYLOAD_HANDLER": "styleguide_example.authentication.services.auth_jwt_response_payload_handler",
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=JWT_EXPIRATION_DELTA_SECONDS),
    "JWT_ALLOW_REFRESH": False,

    "JWT_AUTH_COOKIE": JWT_AUTH_COOKIE,
    "JWT_AUTH_COOKIE_SECURE": True,
    "JWT_AUTH_COOKIE_SAMESITE": JWT_AUTH_COOKIE_SAMESITE,

    "JWT_AUTH_HEADER_PREFIX": JWT_AUTH_HEADER_PREFIX
}
