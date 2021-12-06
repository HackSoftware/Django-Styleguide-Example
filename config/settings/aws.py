from config.env import env

DEFAULT_FILE_STORAGE = env(
    "DEFAULT_FILE_STORAGE",
    default="django.core.files.storage.FileSystemStorage",
)

USE_S3_UPLOAD = env("USE_S3_UPLOAD", default=False)

if USE_S3_UPLOAD:
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

    AWS_FILES_EXPIRY = 60 * 60  # 1 hour. Change this configuration if needed

    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_DOMAIN = (
        AWS_S3_CUSTOM_DOMAIN or f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    )
    MEDIA_URL = f"https://{AWS_S3_DOMAIN}/media/"
