from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.files.models import File
from styleguide_example.files.services import file_generate_private_presigned_post_data

from styleguide_example.api.mixins import ApiAuthMixin


class FileGeneratePrivatePresignedPostApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        presigned_data = file_generate_private_presigned_post_data(
            user=request.user, **serializer.validated_data
        )

        return Response(data=presigned_data)


class FileLocalUploadAPI(ApiAuthMixin, APIView):
    def post(self, request, file_id):
        if settings.USE_S3_UPLOAD:
            raise PermissionDenied('USE_S3_UPLOAD is enabled. Access to this API is forbidden.')

        file = get_object_or_404(File, id=file_id)

        file.file = request.FILES["file"]
        file.save()

        return Response(status=status.HTTP_201_CREATED)
