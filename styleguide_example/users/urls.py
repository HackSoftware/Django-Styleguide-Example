from django.urls import path

from .apis import UserListApi

urlpatterns = [path("", UserListApi.as_view(), name="list")]
