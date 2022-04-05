from enum import Enum


class FileUploadStrategy(Enum):
    DIRECT = "direct"
    PASS_THRU = "pass-thru"


class FileUploadStorage(Enum):
    LOCAL = "local"
    S3 = "s3"
