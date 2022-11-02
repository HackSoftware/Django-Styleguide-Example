from django.urls import path

from .apis import (
    TriggerErrorApi,
    TriggerUnhandledExceptionApi,
    TriggerValidateUniqueErrorApi,
)

urlpatterns = [
    path("trigger/", TriggerErrorApi.as_view()),
    path("trigger/unique/", TriggerValidateUniqueErrorApi.as_view()),
    path("trigger/exception/", TriggerUnhandledExceptionApi.as_view()),
]
