import pathlib

from uuid import uuid4

from django.urls import reverse
from django.conf import settings


def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix

    return f"{uuid4().hex}{extension}"


def file_generate_upload_path(instance, filename):
    return f"files/{instance.file_name}"


def file_generate_local_upload_url(*, file_id: str):
    url = reverse(
        "api:files:upload:pass-thru:local",
        kwargs={"file_id": file_id}
    )

    return f"{settings.SERVER_HOST_DOMAIN}{url}"
