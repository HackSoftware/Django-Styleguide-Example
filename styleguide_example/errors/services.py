from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist,
    PermissionDenied
)
from django.http import Http404

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError as RestValidationError

from styleguide_example.users.models import BaseUser


class NestedSerializer(serializers.Serializer):
    bar = serializers.CharField()


class PlainSerializer(serializers.Serializer):
    foo = serializers.CharField()
    email = serializers.EmailField(min_length=200)

    nested = NestedSerializer()


class ApplicationError(Exception):
    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra


def trigger_error():
    # raise DjangoValidationError("Some error message")

    # raise RestValidationError("Some error message")
    # raise RestValidationError(detail={"error": "Some error message"})

    # raise ObjectDoesNotExist()
    # raise PermissionDenied()
    raise Http404()

    # serializer = PlainSerializer(data={
    #     "email": "foo",
    #     "nested": {}
    # })
    # serializer.is_valid(raise_exception=True)

    # try:
    #     serializer.is_valid(raise_exception=True)
    # except RestValidationError as exc:
    #     breakpoint()
    #     raise

    # raise ApplicationError(
    #     message="You cannot do that operation",
    #     extra={
    #         "type": "RANDOM"
    #     }
    # )
    # raise exceptions.Throttled()
    # raise exceptions.UnsupportedMediaType(media_type="shano/manqk")
    # raise exceptions.NotAcceptable()
    # raise exceptions.MethodNotAllowed(method="SHANO")
    # raise exceptions.NotFound()
    # raise exceptions.PermissionDenied()
    # raise exceptions.NotAuthenticated()
    # raise exceptions.AuthenticationFailed()
    # raise exceptions.ParseError()
    # raise exceptions.ValidationError(set([1, 2, 3]))

    user = BaseUser()
    user.full_clean()
