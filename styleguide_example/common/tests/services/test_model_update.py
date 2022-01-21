import unittest
from unittest.mock import Mock

from styleguide_example.common.services import model_update


class ModelUpdateTests(unittest.TestCase):
    def setUp(self):
        self.instance = Mock(
            field_a=None,
            field_b=None,
            field_c=None
        )

    def test_model_update_does_not_update_if_none_of_the_fields_are_in_the_data(self):
        update_fields = ['non_existing_field']
        data = {'field_a': 'value_a'}

        updated_instance, has_updated = model_update(
            instance=self.instance,
            fields=update_fields,
            data=data
        )

        self.assertEqual(updated_instance, self.instance)
        self.assertFalse(has_updated)

        self.assertIsNone(updated_instance.field_a)
        self.assertIsNone(updated_instance.field_b)
        self.assertIsNone(updated_instance.field_c)

        self.instance.full_clean.assert_not_called()
        self.instance.save.assert_not_called()

    def test_model_update_updates_only_passed_fields_from_data(self):
        update_fields = ['field_a']
        data = {
            'field_a': 'value_a',
            'field_b': 'value_b'
        }

        updated_instance, has_updated = model_update(
            instance=self.instance,
            fields=update_fields,
            data=data
        )

        self.assertTrue(has_updated)

        self.assertEqual(updated_instance.field_a, 'value_a')
        # Even though `field_b` is passed in `data` - it does not get updated
        # because it is not present in the `fields` list.
        self.assertIsNone(updated_instance.field_b)
        # `field_c` remains `None`, because it is not passed anywhere.
        self.assertIsNone(updated_instance.field_c)

        self.instance.full_clean.assert_called_once()
        self.instance.save.assert_called_once_with(update_fields=update_fields)
