from django.test import TestCase

from styleguide_example.blog_examples.f_expressions.db_functions import JSONIncrement
from styleguide_example.blog_examples.models import SomeDataModel


class JSONIncrementTests(TestCase):
    def setUp(self) -> None:
        self.first_entity_stored_field = {"first_key": 1, "second_key": 2, "third_key": 3}
        self.second_entity_stored_field = {"first_key": 4, "second_key": 5, "third_key": 6}
        self.increment_value = 10

    def test_json_increment_in_model(self):
        SomeDataModel.objects.bulk_create(
            [
                SomeDataModel(name="First name", stored_field=self.first_entity_stored_field),
                SomeDataModel(name="Second name", stored_field=self.second_entity_stored_field),
            ]
        )

        first_entity = SomeDataModel.objects.first()
        second_entity = SomeDataModel.objects.last()

        expected_first_entity_stored_field = self.first_entity_stored_field
        actual_first_entity_stored_field = first_entity.stored_field

        expected_second_entity_stored_field = self.second_entity_stored_field
        actual_second_entity_stored_field = second_entity.stored_field

        self.assertEqual(expected_first_entity_stored_field, actual_first_entity_stored_field)
        self.assertEqual(expected_second_entity_stored_field, actual_second_entity_stored_field)

        SomeDataModel.objects.filter(name="First name").update(
            stored_field=JSONIncrement("stored_field__first_key", self.increment_value)
        )

        first_entity = SomeDataModel.objects.first()
        second_entity = SomeDataModel.objects.last()

        """
        Expect only first_entity JSON field with name first_key to be incremented
        """

        expected_first_entity_stored_field = {
            "first_key": self.first_entity_stored_field["first_key"] + self.increment_value,
            "second_key": self.first_entity_stored_field["second_key"],
            "third_key": self.first_entity_stored_field["third_key"],
        }
        actual_first_entity_stored_field = first_entity.stored_field

        expected_second_entity_stored_field = self.second_entity_stored_field
        actual_second_entity_stored_field = second_entity.stored_field

        self.assertEqual(expected_first_entity_stored_field, actual_first_entity_stored_field)
        self.assertEqual(expected_second_entity_stored_field, actual_second_entity_stored_field)
