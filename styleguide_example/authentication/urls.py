from django.urls import path

from .apis import UserLoginApi, UserMeApi

urlpatterns = [
    path(
        'login/',
        UserLoginApi.as_view(),
        name='login'
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    ),
]
