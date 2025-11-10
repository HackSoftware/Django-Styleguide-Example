from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from unittest import mock

from styleguide_example.files.models import File

from styleguide_example.users.services import user_create

from styleguide_example.files.enums import FileUploadStorage


class DirectUploadApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jwt_login_url = reverse("api:authentication:jwt:login")
        self.direct_upload_start_url = reverse("api:files:upload:direct:start")
        self.direct_upload_finish_url = reverse("api:files:upload:direct:finish")
        self.direct_upload_local_url = lambda file: reverse(
            "api:files:upload:direct:local",
            kwargs={"file_id": str(file.id)}
        )

    @override_settings(FILE_UPLOAD_STORAGE=FileUploadStorage.S3, FILE_MAX_SIZE=10)
    def test_direct_upload(self):
        """
        1. Get presigned_post_url from the direct_upload_start endpoint
        1.1. to mock generate the presigned post

        Assert the presigned data
        Assert that the file object is created

        2. Call the finish endpoint and assert that the file is marked as uploaded

        """
        credentials = {
            "email": "test@hacksoft.io",
            "password": "123456"
        }
        user_create(**credentials)

        response = self.client.post(self.jwt_login_url, credentials)

        self.assertEqual(200, response.status_code)

        token = response.data["token"]
        auth_headers = {
            "HTTP_AUTHORIZATION": f"{settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']} {token}"
        }

        file_1 = SimpleUploadedFile(
            name="file_small.txt",
            content=(settings.FILE_MAX_SIZE - 5) * "a".encode(),
            content_type="text/plain"
        )

        file_data = {
            "file_name": file_1.name,
            "file_type": file_1.content_type
        }

        presigned_url = "test_presigned_url"

        presigned_data = {
                    "url": presigned_url,
        }

        with self.subTest("1. Get presigned_post_url from the direct_upload_start endpoint"):

            self.assertEqual(0, File.objects.count())

            with mock.patch(
                "styleguide_example.files.services.s3_generate_presigned_post"
            ) as s3_generate_presigned_post_mock:
                s3_generate_presigned_post_mock.return_value = {**presigned_data}

                response = self.client.post(self.direct_upload_start_url, file_data, **auth_headers)
                file_id = response.data["id"]

                self.assertEqual(200, response.status_code)
                self.assertEqual(presigned_url, response.data["url"])
                self.assertTrue(s3_generate_presigned_post_mock.called)
                self.assertEqual(1, File.objects.count())
                self.assertIsNone(File.objects.last().upload_finished_at)

        with self.subTest("2. Call the finish endpoint and assert that the file is marked as uploaded"):
            response = self.client.post(self.direct_upload_finish_url, {"file_id": file_id})

            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(File.objects.last().upload_finished_at)
