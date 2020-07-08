from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from styleguide_example.api.mixins import ApiErrorsMixin


def trigger_error():
    raise ValidationError('Error from service')


class NestedSerializer(serializers.Serializer):
    bar = serializers.IntegerField()


class TopLevelSerializer(serializers.Serializer):
    foo = NestedSerializer()

    array = serializers.ListField(child=serializers.IntegerField())


class TriggerErrorApi(ApiErrorsMixin, APIView):
    """
    Since we have ApiErrorsMixin,
    The API will fail with 400 Bad Request,
    Instead of 500 Server Error
    """
    def get(self, request):
        serializer = TopLevelSerializer(
            data={
                'foo': {
                    'bar': 'xyz'
                },
                'array': [
                    1, 2, {}
                ]
            }
        )
        serializer.is_valid(raise_exception=True)

        # trigger_error()

        return Response(serializer.validated_data)
