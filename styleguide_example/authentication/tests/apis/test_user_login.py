from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APIClient

from styleguide_example.users.models import BaseUser
from styleguide_example.users.services import user_create


class UserSessionLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.session_login_url = reverse('api:authentication:session:login')
        self.session_logout_url = reverse('api:authentication:session:logout')
        self.me_url = reverse('api:authentication:me')

    def test_non_existing_user_cannot_login(self):
        self.assertEqual(0, BaseUser.objects.count())

        data = {
            'email': 'test@hacksoft.io',
            'password': 'hacksoft'
        }

        response = self.client.post(self.session_login_url, data)

        self.assertEqual(400, response.status_code)

    def test_existing_user_can_login_and_access_apis(self):
        """
        1. Create user
        2. Assert login is OK
        3. Call /api/auth/me
        4. Assert valid response
        """
        credentials = {
            "email": "test@hacksoft.io",
            "password": "password"
        }

        user_create(
            **credentials
        )

        response = self.client.post(self.session_login_url, credentials)

        self.assertEqual(200, response.status_code)

        data = response.data
        self.assertIn("session", data)
        session = data["session"]

        # We have self.client.session
        self.assertIsNotNone(self.client.session)

        response = self.client.get(self.me_url)
        self.assertEqual(200, response.status_code)

        # Now, try without session attached to the client
        client = APIClient()

        response = client.get(self.me_url)
        self.assertEqual(403, response.status_code)

        auth_headers = {
            "HTTP_AUTHORIZATION": f"Session {session}"
        }
        response = client.get(self.me_url, **auth_headers)
        self.assertEqual(200, response.status_code)

    def test_existing_user_can_logout(self):
        """
        1. Create user
        2. Login, can access APIs
        3. Logout, cannot access APIs
        """
        credentials = {
            "email": "test@hacksoft.io",
            "password": "password"
        }

        user_create(
            **credentials
        )

        response = self.client.post(self.session_login_url, credentials)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.me_url)
        self.assertEqual(200, response.status_code)

        self.client.post(self.session_logout_url)

        response = self.client.get(self.me_url)
        self.assertEqual(403, response.status_code)


class UserJwtLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.jwt_login_url = reverse('api:authentication:jwt:login')
        self.jwt_logout_url = reverse('api:authentication:jwt:logout')
        self.me_url = reverse('api:authentication:me')

    def test_non_existing_user_cannot_login(self):
        self.assertEqual(0, BaseUser.objects.count())

        data = {
            'email': 'test@hacksoft.io',
            'password': 'hacksoft'
        }

        response = self.client.post(self.jwt_login_url, data)

        self.assertEqual(400, response.status_code)

    def test_existing_user_can_login_and_access_apis(self):
        """
        1. Create user
        2. Assert login is OK
        3. Call /api/auth/me
        4. Assert valid response
        """
        credentials = {
            "email": "test@hacksoft.io",
            "password": "password"
        }

        user_create(
            **credentials
        )

        response = self.client.post(self.jwt_login_url, credentials)

        self.assertEqual(200, response.status_code)

        data = response.data
        self.assertIn("token", data)
        token = data["token"]

        jwt_cookie = response.cookies.get(settings.JWT_AUTH["JWT_AUTH_COOKIE"])

        self.assertEqual(token, jwt_cookie.value)

        response = self.client.get(self.me_url)
        self.assertEqual(200, response.status_code)

        # Now, try without session attached to the client
        client = APIClient()

        response = client.get(self.me_url)
        self.assertEqual(403, response.status_code)

        auth_headers = {
            "HTTP_AUTHORIZATION": f"{settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']} {token}"
        }
        response = client.get(self.me_url, **auth_headers)
        self.assertEqual(200, response.status_code)

    def test_existing_user_can_logout(self):
        """
        1. Create user
        2. Login, can access APIs
        3. Logout, cannot access APIs
        """
        credentials = {
            "email": "test@hacksoft.io",
            "password": "password"
        }

        user = user_create(
            **credentials
        )

        key_before_logout = user.jwt_key

        response = self.client.post(self.jwt_login_url, credentials)
        self.assertEqual(200, response.status_code)

        response = self.client.get(self.me_url)
        self.assertEqual(200, response.status_code)

        self.client.post(self.jwt_logout_url)

        response = self.client.get(self.me_url)
        self.assertEqual(403, response.status_code)

        user.refresh_from_db()
        key_after_logout = user.jwt_key

        self.assertNotEqual(key_before_logout, key_after_logout)
