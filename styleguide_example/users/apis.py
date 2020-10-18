from rest_framework.views import APIView
from rest_framework.response import Response


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    def get(self, request):
        return Response()
