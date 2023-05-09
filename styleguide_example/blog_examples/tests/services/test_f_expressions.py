from django.test import TestCase

from styleguide_example.blog_examples.f_expressions.service import JSONIncrement
from styleguide_example.blog_examples.models import SomeDataModel


class JSONIncrementTests(TestCase):
    def setUp(self) -> None:
        self.first_entity_stored_field = {"first_key": 1, "second_key": 2, "third_key": 3}
        self.second_entity_stored_field = {"first_key": 4, "second_key": 5, "third_key": 6}
        self.increment_value = 10

    def save_model_entities(self):
        entities = SomeDataModel.objects.bulk_create(
            [
                SomeDataModel(name="First name", stored_field=self.first_entity_stored_field),
                SomeDataModel(name="Second name", stored_field=self.second_entity_stored_field),
            ]
        )
        return entities

    def test_json_increment_in_model(self):
        self.save_model_entities()

        SomeDataModel.objects.filter(name="First name").update(
            stored_field=JSONIncrement("stored_field__first_key", self.increment_value)
        )

        changed_entity = SomeDataModel.objects.first()
        second_entity = SomeDataModel.objects.last()

        self.assertEqual(
            self.first_entity_stored_field["first_key"] + self.increment_value, changed_entity.stored_field["first_key"]
        )
        self.assertEqual(self.second_entity_stored_field["first_key"], second_entity.stored_field["first_key"])
