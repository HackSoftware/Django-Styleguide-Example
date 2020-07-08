from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.api.mixins import ApiErrorsMixin


def trigger_error():
    raise ValidationError('Error from service')


class TriggerErrorApi(ApiErrorsMixin, APIView):
    """
    Since we have ApiErrorsMixin,
    The API will fail with 400 Bad Request,
    Instead of 500 Server Error
    """
    def get(self, request):
        trigger_error()

        return Response()
