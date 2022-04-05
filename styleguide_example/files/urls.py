from django.urls import path, include

from styleguide_example.files.apis import (
    FileDirectUploadApi,

    FilePassThruUploadStartApi,
    FilePassThruUploadFinishApi,
    FilePassThruUploadLocalApi,
)


urlpatterns = [
    path(
        "upload/",
        include(([
            path(
                "direct/",
                FileDirectUploadApi.as_view(),
                name="direct"
            ),
            path(
                "pass-thru/",
                include(([
                    path(
                        "start/",
                        FilePassThruUploadStartApi.as_view(),
                        name="start"
                    ),
                    path(
                        "finish/",
                        FilePassThruUploadFinishApi.as_view(),
                        name="finish"
                    ),
                    path(
                        "local/<str:file_id>/",
                        FilePassThruUploadLocalApi.as_view(),
                        name="local"
                    )
                ], "pass-thru"))
            )
        ], "upload"))
    )
]
