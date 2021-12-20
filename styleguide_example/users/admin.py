from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from styleguide_example.users.models import BaseUser
from styleguide_example.users.services import user_create


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_superuser', 'is_active', 'created_at', 'updated_at')

    search_fields = ('email',)

    list_filter = ('is_active', 'is_admin', 'is_superuser')

    fieldsets = (
        (
            None, {
                'fields': ('email',)
            }
        ),
        (
            "Booleans", {
                "fields": ("is_active", "is_admin", "is_superuser")
            }
        ),
        (
            "Timestamps", {
                "fields": ("created_at", "updated_at")
            }
        )
    )

    readonly_fields = ("created_at", "updated_at", )

    def save_model(self, request, obj, form, change):
        if change:
            return super().save_model(request, obj, form, change)

        try:
            user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
