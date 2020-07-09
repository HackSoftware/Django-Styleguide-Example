from unittest import TestCase

from styleguide_example.api.errors import ErrorFormatter
from styleguide_example.common.apis import TopLevelIntegerSerializer, TopLevelCharSerializer

from django.core.exceptions import ValidationError

class ErrorFormatterTests(TestCase):
    """
    Test how this behaves by passing different versions of drf ValidationError
    """

    def test_error_formatter_with_django_validation_error(self):
        actual = ErrorFormatter(ValidationError('Some error'))()

        expected = {
            'errors': [{
                'message': 'Some error',
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_with_none(self):
        actual = ErrorFormatter(ValidationError(None))()

        expected = {
            'errors': [{
                'message': "['None']",
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_with_message_dict(self):
        actual = ErrorFormatter(ValidationError({
            'foo': ['bar', 'foobar'],
            'Some error': 'error text'
        }))()

        expected = {
            'errors': [{
                'message': {
                    'foo': ['bar', 'foobar'],
                    'Some error': ['error text']
                },
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_with_message_dict_field(self):
        actual = ErrorFormatter(ValidationError({
            'foo': ['bar', 'foobar'],
            'Some error': 'error text',
            'field': 'some message'
        }))()

        expected = {
            'errors': [{
                'message': {
                    'foo': ['bar', 'foobar'],
                    'Some error': ['error text'],
                    'field': ['some message']
                },
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_with_message_dict_field_list(self):
        actual = ErrorFormatter(ValidationError({
            'foo': ['bar', 'foobar'],
            'Some error': 'error text',
            'field': ['some message 1', 'some message 2']
        }))()

        expected = {
            'errors': [{
                'message': {
                    'foo': ['bar', 'foobar'],
                    'Some error': ['error text'],
                    'field': ['some message 1', 'some message 2']
                },
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_with_message_list(self):
        actual = ErrorFormatter(ValidationError(['Some error 1', 'Some error 2']))()

        expected = {
            'errors': [{
                'message': 'Some error 1, Some error 2',
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    # ValidationError(ValidationError(...))

    def test_error_formatter_with_django_validation_error_of_validation_error(self):
        actual = ErrorFormatter(ValidationError(ValidationError('Some error')))()

        expected = {
            'errors': [{
                'message': 'Some error',
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_of_validation_error(self):
        actual = ErrorFormatter(ValidationError(ValidationError(None)))()

        expected = {
            'errors': [{
                'message': "['None']",
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_of_validation_error_with_message_dict(self):
        actual = ErrorFormatter(ValidationError(ValidationError({
            'foo': ['bar', 'foobar'],
            'Some error': 'error text'
        })))()

        expected = {
            'errors': [{
                'message': {
                    'foo': ['bar', 'foobar'],
                    'Some error': ['error text']
                },
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    def test_error_formatter_with_django_validation_error_of_validation_error_with_message_list(self):
        actual = ErrorFormatter(ValidationError(ValidationError(['Some error 1', 'Some error 2'])))()

        expected = {
            'errors': [{
                'message': 'Some error 1, Some error 2',
                'code': 'error'
            }]
        }

        self.assertEqual(actual, expected)

    # Nested errors

    def test_error_formatter_with_nested_errors_int(self):
        serializer = TopLevelIntegerSerializer(
            data = {
                'foo': {
                    'bar': 'xyz'
                },
                'array': [
                    1, 2, {}
                ]
            }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as exc:
            actual = ErrorFormatter(exc)()

            expected = {
                "errors": [
                    {
                        "message": "A valid integer is required.",
                        "code": "invalid",
                        "field": "foo.bar"
                    },
                    {
                        "message": "A valid integer is required.",
                        "code": "invalid",
                        "field": "array.2"
                    }
                ]
            }

            self.assertEqual(actual, expected)

    def test_error_formatter_with_nested_errors_string(self):
        serializer = TopLevelCharSerializer(
            data = {
                'foo': {
                    'bar': {}
                },
                'array': [
                    'foo', {}, 'bar'
                ]
            }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as exc:
            actual = ErrorFormatter(exc)()

            expected = {
                "errors": [
                    {
                        "message": "Not a valid string.",
                        "code": "invalid",
                        "field": "foo.bar"
                    },
                    {
                        "message": "Not a valid string.",
                        "code": "invalid",
                        "field": "array.1"
                    }
                ]
            }

            self.assertEqual(actual, expected)
