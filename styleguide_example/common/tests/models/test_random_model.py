from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from styleguide_example.common.models import RandomModel


class RandomModelTests(TestCase):
    def test_object_save_with_database_constraint_fails_with_validation_error_when_full_cleaned(self):
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        # This should raise a ValidationError when `.full_clean()` is called since Django 4.1
        # https://docs.djangoproject.com/en/4.1/ref/models/instances/#validating-objects
        # This wasn't the case in older Django versions and IntegrityError was raised during the `save()`
        with self.assertRaises(ValidationError):
            obj = RandomModel(start_date=start_date, end_date=end_date)
            obj.full_clean()
            obj.save()

    def test_object_create_with_database_constraint_fails_with_integrity_error(self):
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        # Since this is enforced by a database constraint, it'll fail with IntegrityError
        # rather than a ValidationError
        with self.assertRaises(IntegrityError):
            RandomModel.objects.create(start_date=start_date, end_date=end_date)

    def test_object_can_be_created_when_constraint_is_not_hit(self):
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=1)

        self.assertEqual(0, RandomModel.objects.count())

        RandomModel.objects.create(start_date=start_date, end_date=end_date)

        self.assertEqual(1, RandomModel.objects.count())
