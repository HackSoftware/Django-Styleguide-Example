from django.test import TestCase
from django.core.exceptions import ValidationError, PermissionDenied

from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from styleguide_example.api.mixins import ApiErrorsMixin


class ApiThatRaisesDjangoValidationError(ApiErrorsMixin, APIView):
    def get(self, request):
        raise ValidationError('Some error')


class ApiThatRaisesValueError(ApiErrorsMixin, APIView):
    def get(self, request):
        raise ValueError('Some error')


class ApiThatRaisesDjangoPermissionDenied(ApiErrorsMixin, APIView):
    def get(self, request):
        if not request.user.is_staff:
            raise PermissionDenied('Some error')


class ApiThatRaisesPermissionError(ApiErrorsMixin, APIView):
    def get(self, request):
        raise PermissionError('Some error')


class ApiErrorsMixinTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_django_validation_error_is_transformed_to_drf_validation_error(self):
        request = self.factory.get('/some/path')

        response = ApiThatRaisesDjangoValidationError.as_view()(request)

        self.assertEqual(400, response.status_code)

    def test_value_error_is_transformed_to_drf_validation_error(self):
        request = self.factory.get('/some/path')

        response = ApiThatRaisesValueError.as_view()(request)

        self.assertEqual(400, response.status_code)

    def test_django_permission_denied_is_transformed_to_drf_permission_denied(self):
        request = self.factory.get('/some/path')

        response = ApiThatRaisesDjangoPermissionDenied.as_view()(request)

        self.assertEqual(403, response.status_code)

    def test_permission_error_is_transformed_to_drf_permission_denied(self):
        request = self.factory.get('/some/path')

        response = ApiThatRaisesPermissionError.as_view()(request)

        self.assertEqual(403, response.status_code)
