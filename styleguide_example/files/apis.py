from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.files.models import File
from styleguide_example.files.services import (
    FileDirectUploadService,
    FilePassThruUploadService
)

from styleguide_example.api.mixins import ApiAuthMixin


class FileDirectUploadApi(ApiAuthMixin, APIView):
    def post(self, request):
        service = FileDirectUploadService(
            user=request.user,
            file_obj=request.FILES["file"]
        )
        file = service.create()

        return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)


class FilePassThruUploadStartApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = FilePassThruUploadService(request.user)
        presigned_data = service.start(**serializer.validated_data)

        return Response(data=presigned_data)


class FilePassThruUploadLocalApi(ApiAuthMixin, APIView):
    def post(self, request, file_id):
        file = get_object_or_404(File, id=file_id)

        file_object = request.FILES["file"]

        service = FilePassThruUploadService(request.user)
        file = service.upload_local(file=file, file_object=file_object)

        return Response({"id": file.id})


class FilePassThruUploadFinishApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = serializer.validated_data["file_id"]

        file = get_object_or_404(File, id=file_id)

        service = FilePassThruUploadService(request.user)
        service.finish(file=file)

        return Response({"id": file.id})
