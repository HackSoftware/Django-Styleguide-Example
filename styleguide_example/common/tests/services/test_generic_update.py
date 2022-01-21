import unittest
from unittest.mock import Mock

from styleguide_example.common.services import generic_update


class GenericUpdateTests(unittest.TestCase):
    def test_generic_update_returns_none_if_passed_instance_is_none(self):
        instance = None
        updated_instance = generic_update(instance=instance)

        self.assertIsNone(updated_instance)

    def test_generic_update_returns_none_if_no_update_fields_are_passed(self):
        instance = Mock()
        updated_instance = generic_update(instance=instance)

        self.assertEqual(instance, updated_instance)
        instance.full_clean.assert_not_called()
        instance.save.assert_not_called()

    def test_generic_update_sets_passed_fields_and_executes_full_clean_and_save(self):
        instance = Mock(
            field_a=None,
            field_b=None,
            field_c=None
        )
        fields_to_update = {
            'field_a': 'value_a',
            'field_b': 'value_b',
        }

        self.assertIsNone(instance.field_a)
        self.assertIsNone(instance.field_b)
        self.assertIsNone(instance.field_c)

        updated_instance = generic_update(instance=instance, **fields_to_update)

        instance.full_clean.assert_called_once()
        instance.save.assert_called_once_with(update_fields=['field_a', 'field_b'])

        self.assertEqual(updated_instance.field_a, 'value_a')
        self.assertEqual(updated_instance.field_b, 'value_b')
        # `field_c` is not updated because it is not passed as a field to update
        self.assertIsNone(updated_instance.field_c)
