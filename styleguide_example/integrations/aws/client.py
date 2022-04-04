import boto3

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from typing import Optional


def s3_get_client():
    required_config = [
        settings.AWS_S3_ACCESS_KEY_ID,
        settings.AWS_S3_SECRET_ACCESS_KEY,
        settings.AWS_S3_REGION_NAME,
        settings.AWS_STORAGE_BUCKET_NAME,
        settings.AWS_DEFAULT_ACL,
        settings.AWS_PRESIGNED_EXPIRY
    ]

    for config in required_config:
        if not config:
            raise ImproperlyConfigured(f'AWS not configured. Missing {config}.')

    return boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )


def s3_generate_presigned_post(*, file_path: str, file_type: str) -> Optional[str]:
    s3_client = s3_get_client()

    acl = settings.AWS_DEFAULT_ACL
    expires_in = settings.AWS_PRESIGNED_EXPIRY

    url = s3_client.generate_presigned_post(
        settings.AWS_STORAGE_BUCKET_NAME,
        file_path,
        Fields={
            "acl": acl,
            "Content-Type": file_type
        },
        Conditions=[
            {"acl": acl},
            {"Content-Type": file_type}
        ],
        ExpiresIn=expires_in,
    )

    return url
