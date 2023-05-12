from django.urls import include, path

urlpatterns = [
    path("auth/", include(("styleguide_example.authentication.urls", "authentication"))),
    path("users/", include(("styleguide_example.users.urls", "users"))),
    path("errors/", include(("styleguide_example.errors.urls", "errors"))),
    path("files/", include(("styleguide_example.files.urls", "files"))),
    path(
        "google-oauth2/", include(("styleguide_example.blog_examples.google_login_server_flow.urls", "google-oauth2"))
    ),
]
