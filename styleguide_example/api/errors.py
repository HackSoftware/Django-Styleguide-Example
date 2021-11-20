from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error

from styleguide_example.errors.services import ApplicationError


"""
Error structure:

{
    "message": "Human readable message",
}
"""


def drf_default_with_modifications_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response


# def custom_exception_handler(exc, ctx):
#     if isinstance(exc, DjangoValidationError):
#         exc = exceptions.ValidationError(as_serializer_error(exc))

#     response = exception_handler(exc, ctx)

#     # If unexpected error occurs (server error, etc.)
#     if response is None:

#         if isinstance(exc, ApplicationError):
#             return Response({
#                 "message": exc.message,
#                 "extra": exc.extra,
#                 },
#                 status=400
#             )

#         return response

#     # exception_detail = exc.detail

#     # We want to handle the case, where we throw ValidationError("Some message")
#     # And the detail is ["Some message"]
#     # if isinstance(exception_detail, list):
#     #     response.data = {
#     #         "detail": exception_detail[0]
#     #     }

#     return response
