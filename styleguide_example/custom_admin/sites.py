from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import path, reverse

from styleguide_example.blog_examples.admin_2fa.models import UserTwoFactorAuthData
from styleguide_example.blog_examples.admin_2fa.views import (
    AdminConfirmTwoFactorAuthView,
    AdminSetupTwoFactorAuthView,
)


class AdminSite(admin.AdminSite):
    def get_urls(self):
        base_urlpatterns = super().get_urls()

        extra_urlpatterns = [
            path("setup-2fa/", self.admin_view(AdminSetupTwoFactorAuthView.as_view()), name="setup-2fa"),
            path("confirm-2fa/", self.admin_view(AdminConfirmTwoFactorAuthView.as_view()), name="confirm-2fa"),
        ]

        return extra_urlpatterns + base_urlpatterns

    def login(self, request, *args, **kwargs):
        if request.method != "POST":
            return super().login(request, *args, **kwargs)

        username = request.POST.get("username")

        two_factor_auth_data = UserTwoFactorAuthData.objects.filter(user__email=username).first()

        request.POST._mutable = True
        request.POST[REDIRECT_FIELD_NAME] = reverse("admin:confirm-2fa")

        if two_factor_auth_data is None:
            request.POST[REDIRECT_FIELD_NAME] = reverse("admin:setup-2fa")

        request.POST._mutable = False

        return super().login(request, *args, **kwargs)

    def has_permission(self, request):
        has_perm = super().has_permission(request)

        if not has_perm:
            return has_perm

        two_factor_auth_data = UserTwoFactorAuthData.objects.filter(user=request.user).first()

        allowed_paths = [reverse("admin:confirm-2fa"), reverse("admin:setup-2fa")]

        if request.path in allowed_paths:
            return True

        if two_factor_auth_data is not None:
            two_factor_auth_token = request.session.get("2fa_token")

            return str(two_factor_auth_data.session_identifier) == two_factor_auth_token

        return False
