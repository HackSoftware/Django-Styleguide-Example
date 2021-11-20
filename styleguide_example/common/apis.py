from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers


def trigger_error():
    raise ValidationError('Error from service')


class NestedIntegerSerializer(serializers.Serializer):
    bar = serializers.IntegerField()


class TopLevelIntegerSerializer(serializers.Serializer):
    foo = NestedIntegerSerializer()

    array = serializers.ListField(child=serializers.IntegerField())


class NestedCharSerializer(serializers.Serializer):
    bar = serializers.CharField()


class TopLevelCharSerializer(serializers.Serializer):
    foo = NestedCharSerializer()

    array = serializers.ListField(child=serializers.CharField())


class TriggerErrorApi(APIView):
    """
    Since we have ApiErrorsMixin,
    The API will fail with 400 Bad Request,
    Instead of 500 Server Error
    """
    def get(self, request):
        # serializer = TopLevelIntegerSerializer(
        #     data={
        #         'foo': {
        #             'bar': 'xyz'
        #         },
        #         'array': [
        #             1, 2, {}
        #         ]
        #     }
        # )
        # serializer.is_valid(raise_exception=True)

        serializer = TopLevelCharSerializer(
            data={
                'foo': {
                    'bar': {}
                },
                'array': [
                    'foo', 'bar', {}
                ]
            }
        )
        serializer.is_valid(raise_exception=True)

        # trigger_error()

        # return Response(serializer.validated_data)
        return Response(serializer.validated_data)
