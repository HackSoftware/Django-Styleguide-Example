from django.urls import path

from .apis import TriggerErrorApi


urlpatterns = [
    path(
        "trigger/",
        TriggerErrorApi.as_view()
    )
]
