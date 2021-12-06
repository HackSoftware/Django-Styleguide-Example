from django.contrib import admin

from styleguide_example.files.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ["id", "file_name"]

    ordering = ["-created_at"]
