from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.errors.services import trigger_error


class TriggerErrorApi(APIView):
    def get(self, request):
        trigger_error()

        return Response()
