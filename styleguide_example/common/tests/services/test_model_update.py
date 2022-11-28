from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from styleguide_example.common.factories import RandomModelFactory, SimpleModelFactory
from styleguide_example.common.services import model_update
from styleguide_example.utils.tests import faker


class ModelUpdateTests(TestCase):
    def setUp(self):
        self.model_instance = RandomModelFactory()
        self.simple_object = SimpleModelFactory()
        self.instance = Mock(field_a=None, field_b=None, field_c=None)

    def test_model_update_does_not_update_if_none_of_the_fields_are_in_the_data(self):
        update_fields = ["non_existing_field"]
        data = {"field_a": "value_a"}

        updated_instance, has_updated = model_update(instance=self.instance, fields=update_fields, data=data)

        self.assertEqual(updated_instance, self.instance)
        self.assertFalse(has_updated)

        self.assertIsNone(updated_instance.field_a)
        self.assertIsNone(updated_instance.field_b)
        self.assertIsNone(updated_instance.field_c)

        self.instance.full_clean.assert_not_called()
        self.instance.save.assert_not_called()

    def test_model_update_updates_only_passed_fields_from_data(self):
        update_fields = ["field_a"]
        data = {"field_a": "value_a", "field_b": "value_b"}

        updated_instance, has_updated = model_update(instance=self.instance, fields=update_fields, data=data)

        self.assertTrue(has_updated)

        self.assertEqual(updated_instance.field_a, "value_a")
        # Even though `field_b` is passed in `data` - it does not get updated
        # because it is not present in the `fields` list.
        self.assertIsNone(updated_instance.field_b)
        # `field_c` remains `None`, because it is not passed anywhere.
        self.assertIsNone(updated_instance.field_c)

        self.instance.full_clean.assert_called_once()
        self.instance.save.assert_called_once_with(update_fields=update_fields)

    def test_model_update_updates_many_to_many_fields(self):
        update_fields = ["simple_objects"]
        data = {"simple_objects": [self.simple_object]}

        updated_instance, has_updated = model_update(instance=self.model_instance, fields=update_fields, data=data)

        self.assertEqual(updated_instance, self.model_instance)
        self.assertTrue(has_updated)

        self.assertIn(self.simple_object, updated_instance.simple_objects.all())

    def test_model_update_raises_error_when_called_with_non_existent_field(self):
        update_fields = ["fake_models"]
        data = {"fake_models": [self.simple_object]}

        with self.assertRaisesMessage(ValidationError, "RandomModel has no field named 'fake_models'"):
            updated_instance, has_updated = model_update(instance=self.model_instance, fields=update_fields, data=data)

    def test_model_update_works_with_different_kinds_of_fields(self):
        new_start_date = faker.date_object(end_datetime=self.model_instance.end_date)
        update_fields = ["simple_objects", "start_date"]
        data = {
            "simple_objects": [self.simple_object],
            "start_date": new_start_date,
        }

        updated_instance, has_updated = model_update(instance=self.model_instance, fields=update_fields, data=data)

        self.assertEqual(updated_instance, self.model_instance)
        self.assertTrue(has_updated)

        self.assertEqual(updated_instance.start_date, new_start_date)
        self.assertIn(self.simple_object, updated_instance.simple_objects.all())
