from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from styleguide_example.api.pagination import CursorPaginationService, CursorPagination

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


# TODO: When JWT is resolved, add authenticated version
class UserListApi(APIView):
    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_admin = serializers.NullBooleanField(required=False)
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

        pagination_service = CursorPaginationService()
        pagination: CursorPagination = pagination_service.build_from_query_params(request.query_params)

        users = user_list(filters=filters_serializer.validated_data, pagination=pagination)

        data = self.OutputSerializer(users, many=True).data

        return Response(data)
