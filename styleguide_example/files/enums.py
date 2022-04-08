from enum import Enum


class FileUploadStrategy(Enum):
    STANDARD = "standard"
    DIRECT = "direct"


class FileUploadStorage(Enum):
    LOCAL = "local"
    S3 = "s3"
