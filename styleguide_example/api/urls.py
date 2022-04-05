from django.urls import path, include

urlpatterns = [
    path(
        'auth/', include(('styleguide_example.authentication.urls', 'authentication'))
    ),
    path('users/', include(('styleguide_example.users.urls', 'users'))),
    path('errors/', include(('styleguide_example.errors.urls', 'errors'))),
    path('files/', include(('styleguide_example.files.urls', 'files'))),
]
