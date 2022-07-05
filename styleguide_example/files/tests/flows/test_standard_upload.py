from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from styleguide_example.files.models import File

from styleguide_example.users.models import BaseUser
from styleguide_example.users.services import user_create


class StandardUploadApiTests(TestCase):
    """
    We want to test the following general cases:

    1. Upload a file, below the size limit, assert models gets created accordingly.
    2. Upload a file, above the size limit (patch settings), assert API error, nothing gets created.
    3. Upload a file, equal to the size limit, assert models gets created accordingly.
    """
    def setUp(self):
        self.client = APIClient()

        self.jwt_login_url = reverse("api:authentication:jwt:login")
        self.standard_upload_url = reverse("api:files:upload:standard")

    @override_settings(FILE_MAX_SIZE=10)
    def test_standard_upload(self):
        file_max_size = settings.FILE_MAX_SIZE

        self.assertEqual(0, File.objects.count())
        self.assertEqual(0, BaseUser.objects.count())

        # Create a user
        credentials = {
            "email": "some_email@hacksoft.io",
            "password": "123456"
        }
        user_create(**credentials)

        self.assertEqual(1, BaseUser.objects.count())

        # Log in and get the authorization data needed
        response = self.client.post(self.jwt_login_url, credentials)

        self.assertEqual(200, response.status_code)

        token = response.data["token"]
        auth_headers = {
            "HTTP_AUTHORIZATION": f"{settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']} {token}"
        }

        # Create a small sized file
        file_1 = SimpleUploadedFile(
            name="file_small.txt", content=b"Test", content_type="text/plain"
        )

        with self.subTest("1. Upload a file, below the size limit, assert models gets created accordingly"):
            response = self.client.post(
                self.standard_upload_url, {"file": file_1}, enctype="multipart/form-data", **auth_headers
            )

            self.assertEqual(201, response.status_code)
            self.assertEqual(1, File.objects.count())

        # Create a file above the size limit
        file_2 = SimpleUploadedFile(
            name="file_big.txt", content=(file_max_size + 1) * "a".encode(), content_type="text/plain"
        )

        with self.subTest("2. Upload a file, above the size limit, assert API error, nothing gets created"):
            response = self.client.post(
                self.standard_upload_url, {"file": file_2}, enctype="multipart/form-data", **auth_headers
            )

            self.assertEqual(400, response.status_code)
            self.assertEqual(1, File.objects.count())

        # Create a file equal to the size limit
        file_3 = SimpleUploadedFile(
            name="file_equal.txt", content=file_max_size * "b".encode(), content_type="text/plain"
        )

        with self.subTest("3. Upload a file, equal to the size limit, assert models gets created accordingly"):
            response = self.client.post(
                self.standard_upload_url, {"file": file_3}, enctype="multipart/form-data", **auth_headers
            )

            self.assertEqual(201, response.status_code)
            self.assertEqual(2, File.objects.count())


class StandardUploadAdminTests(TestCase):
    """
    We want to test the following general cases:

    File within size limit:

    1. Create a new file via the Django admin, assert everything gets created (we are using services there).
    2. Update an existing file via the Django admin, assert everything gets updated (we are using services there).

    File not within size limit:

    1. Create a new file via the Django admin, assert error, nothing gets created.
    2. Update an existing fila via the Django admin, assert error, nothing gets created.
    """
