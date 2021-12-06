import logging

import boto3
from botocore.exceptions import ClientError

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from typing import Optional


def get_s3_client():
    required_config = [
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_STORAGE_BUCKET_NAME,
        settings.AWS_FILES_EXPIRY
    ]

    for config in required_config:
        if not config:
            raise ImproperlyConfigured(f'AWS not configured. Missing {config}.')

    return boto3.client(
        service_name="s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def s3_generate_private_presigned_post(*, file_path: str, file_type: str) -> Optional[str]:
    s3_client = get_s3_client()

    try:
        url = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            Fields={"acl": "private", "Content-Type": file_type},
            Conditions=[{"acl": "private"}, {"Content-Type": file_type}],
            ExpiresIn=settings.AWS_FILES_EXPIRY,
        )

    except ClientError as e:
        logging.error(e)
        return None

    return url


def s3_generate_public_presigned_post(*, file_path: str, file_type: str) -> Optional[str]:
    s3_client = get_s3_client()

    try:
        url = s3_client.generate_presigned_post(
            settings.AWS_STORAGE_BUCKET_NAME,
            file_path,
            Fields={"acl": "public", "Content-Type": file_type},
            Conditions=[{"acl": "public"}, {"Content-Type": file_type}],
            ExpiresIn=settings.AWS_FILES_EXPIRY,
        )

    except ClientError as e:
        logging.error(e)
        return None

    return url
