from typing import Dict, Any

from functools import lru_cache

from attrs import define

import boto3

from styleguide_example.common.utils import assert_settings


@define
class S3Credentials:
    access_key_id: str
    secret_access_key: str
    region_name: str
    bucket_name: str
    default_acl: str
    presigned_expiry: int
    max_size: int


@lru_cache
def s3_get_credentials() -> S3Credentials:
    required_config = assert_settings(
        [
            "AWS_S3_ACCESS_KEY_ID",
            "AWS_S3_SECRET_ACCESS_KEY",
            "AWS_S3_REGION_NAME",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_DEFAULT_ACL",
            "AWS_PRESIGNED_EXPIRY",
            "FILE_MAX_SIZE"
        ],
        "S3 credentials not found."
    )

    return S3Credentials(
        access_key_id=required_config["AWS_S3_ACCESS_KEY_ID"],
        secret_access_key=required_config["AWS_S3_SECRET_ACCESS_KEY"],
        region_name=required_config["AWS_S3_REGION_NAME"],
        bucket_name=required_config["AWS_STORAGE_BUCKET_NAME"],
        default_acl=required_config["AWS_DEFAULT_ACL"],
        presigned_expiry=required_config["AWS_PRESIGNED_EXPIRY"],
        max_size=required_config["FILE_MAX_SIZE"]
    )


def s3_get_client():
    credentials = s3_get_credentials()

    return boto3.client(
        service_name="s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region_name
    )


def s3_generate_presigned_post(*, file_path: str, file_type: str) -> Dict[str, Any]:
    credentials = s3_get_credentials()
    s3_client = s3_get_client()

    acl = credentials.default_acl
    expires_in = credentials.presigned_expiry

    """
    TODO: Create a type for the presigned_data
    It looks like this:

    {
        'fields': {
            'Content-Type': 'image/png',
            'acl': 'private',
            'key': 'files/bafdccb665a447468e237781154883b5.png',
            'policy': 'some-long-base64-string',
            'x-amz-algorithm': 'AWS4-HMAC-SHA256',
            'x-amz-credential': 'AKIASOZLZI5FJDJ6XTSZ/20220405/eu-central-1/s3/aws4_request',
            'x-amz-date': '20220405T114912Z',
            'x-amz-signature': '7d8be89aabec12b781d44b5b3f099d07be319b9a41d9a9c804bd1075e1ef5735'
        },
        'url': 'https://django-styleguide-example.s3.amazonaws.com/'
    }
    """
    presigned_data = s3_client.generate_presigned_post(
        credentials.bucket_name,
        file_path,
        Fields={
            "acl": acl,
            "Content-Type": file_type
        },
        Conditions=[
            {"acl": acl},
            {"Content-Type": file_type},
            # As an example, allow file size up to 10 MiB
            # More on conditions, here:
            # https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-HTTPPOSTConstructPolicy.html
            ["content-length-range", 1, credentials.max_size]
        ],
        ExpiresIn=expires_in,
    )

    return presigned_data
