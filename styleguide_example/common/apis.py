from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.api.mixins import ApiErrorsMixin


class TriggerErrorApi(ApiErrorsMixin, APIView):
    def get(self, request):
        return Response()
