from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ApiAuthMixin:
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
