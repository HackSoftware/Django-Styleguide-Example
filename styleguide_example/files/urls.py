from django.urls import path

from styleguide_example.files.apis import (
    FileGeneratePrivatePresignedPostApi,
    FileLocalUploadAPI,
    FileVerifyUploadAPI
)

urlpatterns = [
    path("private-presigned-post/", FileGeneratePrivatePresignedPostApi.as_view()),
    path(
        "<uuid:file_id>/local-upload/",
        FileLocalUploadAPI.as_view(),
    ),
    path(
        "<uuid:file_id>/verify-upload/",
        FileVerifyUploadAPI.as_view(),
    ),
]
