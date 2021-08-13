import unittest

from datetime import datetime, timezone

from rest_framework import serializers

from styleguide_example.common.utils import inline_serializer, make_mock_object


class InlineSerializerTests(unittest.TestCase):
    def test_inline_serializer_creates_a_serializer(self):
        dt = datetime(
            year=2021,
            month=1,
            day=1,
            hour=1,
            minute=1,
            second=1,
            microsecond=1,
            tzinfo=timezone.utc
        )
        expected_dt = "2021-01-01T01:01:01.000001Z"

        obj = make_mock_object(
            foo=1,
            bar="bar",
            dt=dt
        )

        serializer = inline_serializer(fields={
            "foo": serializers.IntegerField(),
            "bar": serializers.CharField(),
            "dt": serializers.DateTimeField()
        })

        with self.subTest("Output serialization"):
            result = serializer.to_representation(obj)
            expected = {
                "foo": 1,
                "bar": "bar",
                "dt": expected_dt
            }

            self.assertEqual(expected, result)

        with self.subTest("Input serialization"):
            payload = {
                "foo": 1,
                "bar": "bar",
                "dt": expected_dt
            }

            result = serializer.to_internal_value(payload)
            expected = {
                "foo": 1,
                "bar": "bar",
                "dt": dt
            }

            self.assertEqual(expected, result)

    def test_inline_serializer_passes_kwargs(self):
        obj = make_mock_object(
            foo=1,
        )

        serializer = inline_serializer(many=True, fields={
            "foo": serializers.IntegerField(),
        })

        objects = [obj]

        with self.subTest("Output serialization"):
            result = serializer.to_representation(objects)
            expected = [{
                "foo": 1
            }]

            self.assertEqual(expected, result)

        with self.subTest("Input serialization"):
            payload = [{
                "foo": 1,
            }]

            result = serializer.to_internal_value(payload)
            expected = [{
                "foo": 1
            }]

            self.assertEqual(expected, result)
