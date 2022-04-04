from django.urls import path

from styleguide_example.files.apis import (
    FileDirectUploadApi,

    FilePassThruUploadStartApi,
    FilePassThruUploadFinishApi,
)


urlpatterns = [
    path("upload/direct/", FileDirectUploadApi.as_view()),
    path("upload/pass-thru/start/", FilePassThruUploadStartApi.as_view()),
    path("upload/pass-thru/finish/", FilePassThruUploadFinishApi.as_view()),
]
