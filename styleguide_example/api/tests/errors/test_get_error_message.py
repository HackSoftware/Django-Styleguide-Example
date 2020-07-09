from unittest import TestCase

from styleguide_example.api.errors import get_error_message

from django.core.exceptions import ValidationError, PermissionDenied


class GetErrorMessageTests(TestCase):
    """
    Write some initial test cases for how get_error_message behaves with:

    1. Django ValidationError
    2. Python's ValueError, PermissionDenied
    3. A standard default Exception
    """
    def test_get_error_message_with_django_validation_error(self):
        self.assertEqual('Some error', get_error_message(ValidationError('Some error')))

    def test_get_error_message_with_django_validation_error_none(self):
        self.assertEqual('[\'None\']', get_error_message(ValidationError(None)))

    def test_get_error_message_with_django_validation_error_with_message_dict(self):
        self.assertEqual(
            {
                'foo': ['bar', 'foobar'],
                'Some error': ['error text']
            },
            get_error_message(ValidationError({
                'foo': ['bar', 'foobar'],
                'Some error': 'error text'
            }))
        )

    def test_get_error_message_with_django_validation_error_with_message_list(self):
        self.assertEqual(
            'Some error 1, Some error 2',
            get_error_message(ValidationError(['Some error 1', 'Some error 2'])))

    def test_get_error_message_with_django_permission_denied(self):
        self.assertEqual('Some error', get_error_message(PermissionDenied('Some error')))

    def test_get_error_message_with_value_error(self):
        self.assertEqual('Some error', get_error_message(ValueError('Some error')))

    def test_get_error_message_with_permission_error(self):
        self.assertEqual('Some error', get_error_message(PermissionError('Some error')))

    def test_get_error_message_with_standard_default_exception(self):
        self.assertEqual('Some error', get_error_message(Exception('Some error')))
