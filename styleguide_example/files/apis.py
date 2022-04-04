from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.files.models import File
from styleguide_example.files.services import (
    file_create_for_direct_upload,
    file_pass_thru_upload_start,
    file_pass_thru_upload_finish,
)

from styleguide_example.api.mixins import ApiAuthMixin


class FileDirectUploadApi(ApiAuthMixin, APIView):
    def post(self, request):
        file_object = request.FILES["file"]

        file = file_create_for_direct_upload(
           file_object=file_object,
           user=request.user
        )

        return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)


class FilePassThruUploadStartApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        presigned_data = file_pass_thru_upload_start(
            user=request.user,
            **serializer.validated_data
        )

        return Response(data=presigned_data)


class FilePassThruUploadFinishApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = serializer.validated_data["file_id"]

        file = get_object_or_404(File, id=file_id)

        file = file_pass_thru_upload_finish(
            file=file,
            user=request.user
        )

        return Response({"id": file.id})
