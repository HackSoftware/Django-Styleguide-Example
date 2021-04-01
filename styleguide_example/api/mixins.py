from importlib import import_module

from django.core.exceptions import ValidationError
from django.conf import settings

from django.contrib import auth

from rest_framework import exceptions as rest_exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from styleguide_example.api.errors import get_error_message


def get_auth_header(headers):
    value = headers.get('Authorization')

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """
    def enforce_csrf(self, request):
        return

    def authenticate(self, request):
        auth_result = super().authenticate(request)

        if auth_result is None:
            auth_header = get_auth_header(request.headers)

            if auth_header is None:
                return auth_result

            auth_type, auth_value = auth_header

            if auth_type != 'Session':
                return auth_result

            engine = import_module(settings.SESSION_ENGINE)
            SessionStore = engine.SessionStore
            session_key = auth_value

            request.session = SessionStore(session_key)
            user = auth.get_user(request)

            return user, None

        return auth_result


class ApiAuthMixin:
    authentication_classes = (CsrfExemptedSessionAuthentication, )
    permission_classes = (IsAuthenticated, )


class ApiErrorsMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
