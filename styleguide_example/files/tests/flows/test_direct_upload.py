from django.test import TestCase


class DirectUploadApiTests(TestCase):
    """
    We want to test the following:

    1. A start-upload-finish cycle, where we patch the presign generation with local upload storage.
    """
