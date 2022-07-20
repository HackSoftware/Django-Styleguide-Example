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
    def setUp(self):
        self.client = APIClient()

        self.admin_upload_file_url = reverse("admin:files_file_add")
        self.admin_files_list_url = reverse("admin:files_file_changelist")
        self.admin_update_file_url = lambda file: reverse(
            "admin:files_file_change",
            kwargs={"object_id": str(file.id)}
        )

    @override_settings(FILE_MAX_SIZE=10)
    def test_standard_admin_upload_and_update(self):
        file_max_size = settings.FILE_MAX_SIZE

        self.assertEqual(0, File.objects.count())

        # Create a superuser
        credentials = {
            "email": "admin_email@hacksoft.io",
            "password": "123456",
            "is_admin": True,
            "is_superuser": True
        }
        user = BaseUser.objects.create(**credentials)

        self.assertEqual(1, BaseUser.objects.count())

        file_1 = SimpleUploadedFile(
            name="first_file.txt", content=b"Test!", content_type="text/plain"
        )

        data_file_1 = {
            "file": file_1,
            "uploaded_by": user.id
        }

        # Log in with the superuser account
        self.client.force_login(user)

        with self.subTest("1. Create a new file via the Django admin, assert everything gets created"):
            response = self.client.post(self.admin_upload_file_url, data_file_1)
            successfully_uploaded_file = File.objects.last()

            self.assertEqual(302, response.status_code)
            self.assertEqual(self.admin_files_list_url, response.url)
            self.assertEqual(1, File.objects.count())
            self.assertEqual(file_1.name, successfully_uploaded_file.original_file_name)

        file_2 = SimpleUploadedFile(
            name="second_file.txt", content=(file_max_size - 1) * "a".encode(), content_type="text/plain"
        )

        data_file_2 = {
            "file": file_2,
            "uploaded_by": user.id
        }

        with self.subTest("2. Update an existing file via the Django admin, assert everything gets updated"):
            response = self.client.post(self.admin_update_file_url(successfully_uploaded_file), data_file_2)

            self.assertEqual(302, response.status_code)
            self.assertRedirects(response, self.admin_files_list_url)
            self.assertEqual(1, File.objects.count())
            self.assertEqual(file_2.name, File.objects.last().original_file_name)

        file_3 = SimpleUploadedFile(
            name="oversized_file.txt", content=(file_max_size + 10) * "b".encode(), content_type="text/plain"
        )

        data_oversized_file = {
            "file": file_3,
            "uploaded_by": user.id
        }

        with self.subTest("3. Create a new oversized file via the Django admin, assert error, nothing gets created"):
            response = self.client.post(self.admin_upload_file_url, data_oversized_file)
            response_2 = self.client.get(response.url)

            self.assertContains(response_2, "File is too large")
            self.assertEqual(1, File.objects.count())
            self.assertEqual(file_2.name, File.objects.last().original_file_name)

        file_4 = SimpleUploadedFile(
            name="new_oversized_file.txt", content=(file_max_size + 20) * "c".encode(), content_type="text/plain"
        )

        data_new_oversized_file = {
            "file": file_4,
            "uploaded_by": user.id
        }

        with self.subTest(
            "4. Update an existing file with an oversized one via the Django admin, assert error, nothing gets created"
        ):
            response = self.client.post(self.admin_update_file_url(File.objects.last()), data_new_oversized_file)
            response_2 = self.client.get(response.url)

            self.assertContains(response_2, "File is too large")
            self.assertEqual(1, File.objects.count())
            self.assertEqual(file_2.name, File.objects.last().original_file_name)
