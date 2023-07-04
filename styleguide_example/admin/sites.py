from django.contrib import admin
from django.urls import path

from styleguide_example.blog_examples.admin_2fa.views import AdminSetupTwoFactorAuthView


class AdminSite(admin.AdminSite):
    def get_urls(self):
        base_urlpatterns = super().get_urls()

        extra_urlpatterns = [
            path("setup-2fa/", self.admin_view(AdminSetupTwoFactorAuthView.as_view()), name="setup-2fa")
        ]

        return extra_urlpatterns + base_urlpatterns
