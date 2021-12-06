import pathlib

from django.conf import settings


def file_generate_upload_path(instance, filename):
    extension = pathlib.Path(filename).suffix

    return f"files/{instance.id}{extension}"


def file_generate_local_upload_url(*, file_id: str):
    return f"{settings.SERVER_HOST_DOMAIN}/api/files/images/{file_id}/local-upload/"
