from django.urls import path

from .apis import UserLoginApi, UserLogoutApi, UserMeApi

urlpatterns = [
    path(
        'login/',
        UserLoginApi.as_view(),
        name='login'
    ),
    path(
        'logout/',
        UserLogoutApi.as_view(),
        name='logout'
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    ),
]
