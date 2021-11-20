from importlib import import_module

from django.conf import settings

from django.contrib import auth

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BaseAuthentication


def get_auth_header(headers):
    value = headers.get('Authorization')

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


class SessionAsHeaderAuthentication(BaseAuthentication):
    """
    In case we are dealing with issues like Safari not supporting SameSite=None,
    And the client passes the session as Authorization header:

    Authorization: Session 7wvz4sxcp3chm9quyw015n6ryre29b3u

    Run the standard Django auth & try obtaining user.
    """
    def authenticate(self, request):
        auth_header = get_auth_header(request.headers)

        if auth_header is None:
            return None

        auth_type, auth_value = auth_header

        if auth_type != 'Session':
            return None

        engine = import_module(settings.SESSION_ENGINE)
        SessionStore = engine.SessionStore
        session_key = auth_value

        request.session = SessionStore(session_key)
        user = auth.get_user(request)

        return user, None


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """
    def enforce_csrf(self, request):
        return


class ApiAuthMixin:
    authentication_classes = (CsrfExemptedSessionAuthentication, SessionAsHeaderAuthentication)
    permission_classes = (IsAuthenticated, )
