from django.contrib import admin

from styleguide_example.emails.models import Email
from styleguide_example.emails.services import email_send_all


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "to", "status", "sent_at"]
    actions = ["send_email"]

    def get_queryset(self, request):
        """
        We want to defer the `html` and `plain_text` fields,
        since we are not showing them in the list & we don't need to fetch them.

        Potentially, those fields can be quite heavy.
        """
        queryset = super().get_queryset(request)
        return queryset.defer("html", "plain_text")

    @admin.action(description="Send selected emails.")
    def send_email(self, request, queryset):
        email_send_all(queryset)
