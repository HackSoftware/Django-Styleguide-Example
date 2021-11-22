from rest_framework.views import APIView
from rest_framework.response import Response

from styleguide_example.api.exception_handlers import (
    drf_default_with_modifications_exception_handler,
    hacksoft_proposed_exception_handler
)

from styleguide_example.errors.services import trigger_errors


class TriggerErrorApi(APIView):
    def get(self, request):
        data = {
            "drf_default_with_modifications": trigger_errors(drf_default_with_modifications_exception_handler),
            "hacksoft_proposed": trigger_errors(hacksoft_proposed_exception_handler)
        }

        return Response(data)
