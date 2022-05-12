from django.conf import settings
from django.urls import path, include

from styleguide_example.files.apis import (
    FileStandardUploadApi,

    FileDirectUploadStartApi,
    FileDirectUploadFinishApi,
    FileDirectUploadLocalApi,
)
from styleguide_example.files.enums import FileUploadStorage


direct_upload_urls = [
    path("start/", FileDirectUploadStartApi.as_view(), name="start"),
    path("finish/", FileDirectUploadFinishApi.as_view(), name="finish"),
]

if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.LOCAL:
    direct_upload_urls.append(
        path("local/<str:file_id>/", FileDirectUploadLocalApi.as_view(), name="local")
    )


urlpatterns = [
    path(
        "upload/",
        include(([
            path(
                "standard/",
                FileStandardUploadApi.as_view(),
                name="standard"
            ),
            path(
                "direct/",
                include((direct_upload_urls, "direct"))
            )
        ], "upload"))
    )
]
