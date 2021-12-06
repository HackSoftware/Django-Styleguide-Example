from django.conf import settings
from django.db import transaction

from styleguide_example.files.models import File
from styleguide_example.files.utils import (
    file_generate_upload_path,
    file_generate_local_upload_url
)

from styleguide_example.integrations.aws.client import s3_generate_private_presigned_post

from styleguide_example.users.models import BaseUser


def file_create_for_upload(*, user: BaseUser, file_name: str, file_type: str) -> File:
    image = File(
        file_name=file_name,
        file_type=file_type,
        uploaded_by=user,
        file=None
    )
    image.full_clean()
    image.save()

    return image


@transaction.atomic
def file_generate_private_presigned_post_data(*, request, file_name: str, file_type: str):
    user = request.user

    file = file_create_for_upload(user=user, file_name=file_name, file_type=file_type)

    if settings.USE_S3_UPLOAD:
        upload_path = file_generate_upload_path(file, file.file_name)

        presigned_data = s3_generate_private_presigned_post(
            file_path=upload_path, file_type=file.file_type
        )

        """
        Setting the file.file path to be the s3 upload path without uploading the file.
        The actual file upload will be done by the FE.
        """
        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()
    else:
        """
        Use "Token {user.auth_token} if you're using Token Authentication
        """
        presigned_data = {
            "url": file_generate_local_upload_url(file_id=file.id),
            "params": {"headers": {"Authorization": f"Session {request.session.session_key}"}},
        }

    return {"identifier": file.id, **presigned_data}
