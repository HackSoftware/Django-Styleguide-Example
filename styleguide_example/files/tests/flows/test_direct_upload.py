from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient


class DirectUploadApiTests(TestCase):
    """
    We want to test the following:

    1. A start-upload-finish cycle, where we patch the presign generation with local upload storage.
    """
    def setUp(self):
        self.client = APIClient()

        self.direct_upload_start_url = reverse("api:files:upload:direct:start")
        self.direct_upload_finish_url = reverse("api:files:upload:direct:finish")
        self.direct_upload_local_url = lambda file: reverse(
            "api:files:upload:direct:local",
            kwargs={"file_id": str(file.id)}
        )

    def test_direct_upload(self):
        pass
