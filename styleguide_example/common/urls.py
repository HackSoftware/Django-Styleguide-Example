from django.urls import path

from .apis import TriggerErrorApi


urlpatterns = [
    path('trigger-error/', TriggerErrorApi.as_view(), name='trigger-error'),
]
