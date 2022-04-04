from django.urls import path

from styleguide_example.files.apis import (
    FileDirectUploadApi,

    FileGeneratePrivatePresignedPostApi,
    FileVerifyUploadAPI,
)

urlpatterns = [
    path("upload/direct/", FileDirectUploadApi.as_view()),
    path("private-presigned-post/", FileGeneratePrivatePresignedPostApi.as_view()),
    path(
        "<int:file_id>/verify-upload/",
        FileVerifyUploadAPI.as_view(),
    ),
]
