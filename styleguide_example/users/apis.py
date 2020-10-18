from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from styleguide_example.api.mixins import ApiErrorsMixin

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


# TODO: When JWT is resolved, add authenticated version
class UserListApi(ApiErrorsMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.BooleanField(required=False)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = (
                'id',
                'email',
                'is_admin'
            )

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        data = self.OutputSerializer(users, many=True).data

        return Response(data)
