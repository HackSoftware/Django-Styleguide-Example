from django.urls import path

from styleguide_example.blog_examples.google_login_server_flow.sdk.apis import (
    GoogleLoginApi,
    GoogleLoginRedirectApi,
)

urlpatterns = [
    path("callback/", GoogleLoginApi.as_view(), name="callback-sdk"),
    path("redirect/", GoogleLoginRedirectApi.as_view(), name="redirect-sdk"),
]
