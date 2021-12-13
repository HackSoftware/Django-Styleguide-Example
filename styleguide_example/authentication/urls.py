from django.urls import path, include

from .apis import (
    UserSessionLoginApi,
    UserSessionLogoutApi,
    UserMeApi,
)

urlpatterns = [
    path(
        'session/',
        include(([
            path(
                'login/',
                UserSessionLoginApi.as_view(),
                name='login'
            ),
            path(
                'logout/',
                UserSessionLogoutApi.as_view(),
                name='logout'
            )

        ], "session"))
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    )
]
