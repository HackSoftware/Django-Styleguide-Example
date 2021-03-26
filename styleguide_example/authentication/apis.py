from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.api.mixins import ApiAuthMixin

from styleguide_example.users.selectors import user_get_login_data


class UserLoginApi(APIView):
    pass


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)
