from django.urls import path

from .apis import UserLoginApi

urlpatterns = [
    path(
        'login/',
        UserLoginApi.as_view(),
        name='login'
    )
]
