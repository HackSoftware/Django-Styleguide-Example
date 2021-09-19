from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError

from styleguide_example.common.models import RandomModel


class RandomModelTests(TestCase):
    def test_object_save_with_database_constraint_fails_with_integrity_error(self):
        start_date = timezone.now().date()
        end_date = start_date - timedelta(days=1)

        # Since this is enforced by a database constraint, it'll fail with IntegrityError
        # rather than a ValidationError
        with self.assertRaises(IntegrityError):
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
