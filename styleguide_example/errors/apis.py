import structlog
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.api.exception_handlers import (
    drf_default_with_modifications_exception_handler,
    hacksoft_proposed_exception_handler,
)
from styleguide_example.errors.services import trigger_errors
from styleguide_example.users.services import user_create

logger = structlog.get_logger(__name__)


class TriggerErrorApi(APIView):
    def get(self, request):
        data = {
            "drf_default_with_modifications": trigger_errors(drf_default_with_modifications_exception_handler),
            "hacksoft_proposed": trigger_errors(hacksoft_proposed_exception_handler),
        }

        return Response(data)


class TriggerValidateUniqueErrorApi(APIView):
    def get(self, request):
        # Due to the fiddling with transactions, this example a different API
        user_create(email="unique@hacksoft.io", password="user")
        user_create(email="unique@hacksoft.io", password="user")

        return Response()


class TriggerUnhandledExceptionApi(APIView):
    def get(self, request):
        log = logger.bind()

        try:
            raise Exception("Oops")
        except Exception:
            log.exception("unhandled_exception")
            raise

        return Response()
