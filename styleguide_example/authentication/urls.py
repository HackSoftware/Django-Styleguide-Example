from django.urls import path, include

from .apis import (
    UserSessionLoginApi,
    UserSessionLogoutApi,

    UserJwtLoginApi,
    UserJwtLogoutApi,

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
        'jwt/',
        include(([
            path(
                "login/",
                UserJwtLoginApi.as_view(),
                name="login"
            ),
            path(
                "logout/",
                UserJwtLogoutApi.as_view(),
                name="logout"
            )
        ], "jwt"))
    ),
    path(
        'me/',
        UserMeApi.as_view(),
        name='me'
    )
]
