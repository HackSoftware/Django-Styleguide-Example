import mimetypes

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from styleguide_example.files.models import File
from styleguide_example.files.utils import (
    file_generate_upload_path,
    file_generate_local_upload_url
)

from styleguide_example.integrations.aws.client import s3_generate_presigned_post

from styleguide_example.users.models import BaseUser

from styleguide_example.files.utils import file_generate_name


def file_create_for_direct_upload(
    *,
    user: BaseUser,
    file_object,
    file_name: str = "",
    file_type: str = "",
) -> File:
    if not file_name:
        file_name = file_object.name

    if not file_type:
        file_type, encoding = mimetypes.guess_type(file_name)

        if file_type is None:
            file_type = ""

    obj = File(
        file=file_object,
        original_file_name=file_name,
        file_name=file_generate_name(file_name),
        file_type=file_type,
        uploaded_by=user,
        upload_finished_at=timezone.now()
    )

    obj.full_clean()
    obj.save()

    return obj


def file_update_for_direct_upload(
    *,
    file: File,
    user: BaseUser,
    file_object,
    file_name: str = "",
    file_type: str = "",
) -> File:
    if not file_name:
        file_name = file_object.name

    if not file_type:
        file_type, encoding = mimetypes.guess_type(file_name)

        if file_type is None:
            file_type = ""

    file.file = file_object
    file.original_file_name = file_name
    file.file_name = file_generate_name(file_name)
    file.file_type = file_type
    file.uploaded_by = user
    file.upload_finished_at = timezone.now()

    file.full_clean()
    file.save()

    return file


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
def file_pass_thru_upload_start(
    *,
    user: BaseUser,
    file_name: str,
    file_type: str
):
    file = File(
        original_file_name=file_name,
        file_name=file_generate_name(file_name),
        file_type=file_type,
        uploaded_by=user,
        file=None
    )
    file.full_clean()
    file.save()

    if settings.FILE_UPLOAD_STORAGE == "s3":
        upload_path = file_generate_upload_path(file, file.file_name)

        presigned_data = s3_generate_presigned_post(
            file_path=upload_path, file_type=file.file_type
        )

        """
        TODO: Why are we doing this?

        Setting the file.file path to be the s3 upload path without uploading the file.
        The actual file upload will be done by the FE.
        """
        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()
    else:
        # direct
        pass

    return {"id": file.id, **presigned_data}


@transaction.atomic
def file_pass_thru_upload_finish(
    *,
    user: BaseUser,
    file: File
) -> File:
    # Potentially, check against user

    file.upload_finished_at = timezone.now()
    file.full_clean()
    file.save()

    return file


@transaction.atomic
def file_generate_presigned_post_data(*, request, file_name: str, file_type: str):
    user = request.user

    file = file_create_for_upload(user=user, file_name=file_name, file_type=file_type)

    if settings.USE_S3_UPLOAD:
        upload_path = file_generate_upload_path(file, file.file_name)

        presigned_data = s3_generate_presigned_post(
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
