from django.contrib import admin
from django.utils.html import format_html

from styleguide_example.blog_examples.admin_2fa.models import UserTwoFactorAuthData


@admin.register(UserTwoFactorAuthData)
class UserTwoFactorAuthDataAdmin(admin.ModelAdmin):
    """
    This admin is for example purposes and ease of development and debugging.
    Leaving this admin in production is a security risk.

    Please refer to the following blog post for more information:
    https://hacksoft.io/blog/adding-required-two-factor-authentication-2fa-to-the-django-admin
    """

    def qr_code(self, obj):
        return format_html(obj.generate_qr_code())

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ["user", "otp_secret", "qr_code"]
        else:
            return ()
