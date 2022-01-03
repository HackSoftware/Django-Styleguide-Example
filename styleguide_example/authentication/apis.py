from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from rest_framework_jwt.views import ObtainJSONWebTokenView

from styleguide_example.api.mixins import ApiAuthMixin

from styleguide_example.authentication.services import auth_logout

from styleguide_example.users.selectors import user_get_login_data


class UserSessionLoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({
            'session': session_key,
            'data': data
        })


class UserSessionLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        # We are redefining post so we can change the response status on success
        # Mostly for consistency with the session-based API
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            response.status_code = status.HTTP_200_OK

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH['JWT_AUTH_COOKIE'] is not None:
            response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)
