from django.db import models
from django.conf import settings

from styleguide_example.common.models import BaseModel

from styleguide_example.users.models import BaseUser

from styleguide_example.files.utils import file_generate_upload_path


class File(BaseModel):
    file = models.FileField(upload_to=file_generate_upload_path, null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(null=True, blank=True)
    uploaded_by = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    @property
    def url(self):
        if settings.USE_S3_UPLOAD:
            return self.file.url

        return f"{settings.SERVER_HOST_DOMAIN}{self.file.url}"
