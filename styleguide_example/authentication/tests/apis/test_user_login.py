from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from styleguide_example.users.models import BaseUser


class UserLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_non_existing_user_cannot_login(self):
        self.assertEqual(0, BaseUser.objects.count())

        url = reverse('api:authentication:login')
        data = {
            'email': 'test@hacksoft.io',
            'password': 'hacksoft'
        }

        response = self.client.post(url, data)

        # {'detail': ErrorDetail(string='No active account found with the given credentials', code='no_active_account')}

        self.assertEqual(401, response.status_code)

    def test_existing_user_can_login_and_access_apis(self):
        """
        1. Create user
        2. Assert login is OK
        3. Call /api/auth/me
        4. Assert valid response
        """
