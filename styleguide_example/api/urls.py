from django.urls import path, include

urlpatterns = [
    path(
        'auth/', include(('styleguide_example.authentication.urls', 'authentication'))
    ),
    path('common/', include(('styleguide_example.common.urls', 'common'))),
    path('users/', include(('styleguide_example.users.urls', 'users'))),
]
