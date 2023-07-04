from django.contrib import admin
from django.utils.html import format_html

from styleguide_example.blog_examples.admin_2fa.models import UserTwoFactorAuthData


@admin.register(UserTwoFactorAuthData)
class UserTwoFactorAuthDataAdmin(admin.ModelAdmin):
    def qr_code(self, obj):
        return format_html(obj.generate_qr_code())

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ["user", "otp_secret", "qr_code"]
        else:
            return ()
