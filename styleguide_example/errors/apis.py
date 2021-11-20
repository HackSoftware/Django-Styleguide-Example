from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.errors.services import trigger_errors


class TriggerErrorApi(APIView):
    def get(self, request):
        result = trigger_errors()

        return Response(result)
