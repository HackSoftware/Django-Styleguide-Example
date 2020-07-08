from django.urls import path, include

urlpatterns = [
    path(
        'auth/', include(('styleguide_example.authentication.urls', 'authentication'))
    ),
    path('common/', include(('styleguide_example.common.urls', 'common')))
]
