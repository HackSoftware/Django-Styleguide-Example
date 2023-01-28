from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from styleguide_example.blog_examples.models import (
    TimestampsOpinionated,
    TimestampsWithAuto,
    TimestampsWithAutoAndDefault,
    TimestampsWithDefault,
)


class TimestampsTests(TestCase):
    def test_timestamps_with_auto_behavior(self):
        """
        Timestamps are set automatically
        """
        obj = TimestampsWithAuto()
        obj.full_clean()
        obj.save()

        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

        self.assertNotEqual(obj.created_at, obj.updated_at)

        """
        Timestamps cannot be overridden
        """
        timestamp = timezone.now() - timedelta(days=1)

        obj = TimestampsWithAuto(created_at=timestamp, updated_at=timestamp)
        obj.full_clean()
        obj.save()

        self.assertNotEqual(timestamp, obj.created_at)
        self.assertNotEqual(timestamp, obj.updated_at)

        """
        updated_at gets auto updated, while created_at stays the same
        """
        obj = TimestampsWithAuto()
        obj.full_clean()
        obj.save()

        original_created_at = obj.created_at
        original_updated_at = obj.updated_at

        obj.save()
        # Get a fresh object
        obj = TimestampsWithAuto.objects.get(id=obj.id)

        self.assertEqual(original_created_at, obj.created_at)
        self.assertNotEqual(original_updated_at, obj.updated_at)

    def test_timestamps_with_mixed_behavior(self):
        """
        Timestamps are set automatically / by default
        """
        obj = TimestampsWithAutoAndDefault()
        obj.full_clean()
        obj.save()

        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

        self.assertNotEqual(obj.created_at, obj.updated_at)

        """
        Some timestamps can be overridden
        """
        timestamp = timezone.now() - timedelta(days=1)

        obj = TimestampsWithAutoAndDefault(created_at=timestamp, updated_at=timestamp)
        obj.full_clean()
        obj.save()

        # This is default
        self.assertEqual(timestamp, obj.created_at)
        # This is auto_now
        self.assertNotEqual(timestamp, obj.updated_at)

        """
        updated_at gets auto updated, while created_at stays the same
        """
        obj = TimestampsWithAutoAndDefault()
        obj.full_clean()
        obj.save()

        original_created_at = obj.created_at
        original_updated_at = obj.updated_at

        obj.save()
        # Get a fresh object
        obj = TimestampsWithAutoAndDefault.objects.get(id=obj.id)

        self.assertEqual(original_created_at, obj.created_at)
        self.assertNotEqual(original_updated_at, obj.updated_at)

    def test_timestamps_with_default_behavior(self):
        """
        Timestamps are set by default
        """
        obj = TimestampsWithDefault()
        obj.full_clean()
        obj.save()

        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

        self.assertNotEqual(obj.created_at, obj.updated_at)

        """
        Both timestamps can be overridden
        """
        timestamp = timezone.now() - timedelta(days=1)

        obj = TimestampsWithDefault(created_at=timestamp, updated_at=timestamp)
        obj.full_clean()
        obj.save()

        self.assertEqual(timestamp, obj.created_at)
        self.assertEqual(timestamp, obj.updated_at)
        # And by transitivity
        self.assertEqual(obj.created_at, obj.updated_at)

        """
        created_at / updated_at are not auto updated
        """
        obj = TimestampsWithDefault()
        obj.full_clean()
        obj.save()

        original_created_at = obj.created_at
        original_updated_at = obj.updated_at

        obj.save()
        # Get a fresh object
        obj = TimestampsWithDefault.objects.get(id=obj.id)

        self.assertEqual(original_created_at, obj.created_at)
        self.assertEqual(original_updated_at, obj.updated_at)

    def test_timestamps_with_opinionated_behavior(self):
        """
        created_at is only set by default
        """
        obj = TimestampsOpinionated()
        obj.full_clean()
        obj.save()

        self.assertIsNotNone(obj.created_at)
        self.assertIsNone(obj.updated_at)

        """
        Both timestamps can be overridden
        """
        timestamp = timezone.now() - timedelta(days=1)

        obj = TimestampsOpinionated(created_at=timestamp, updated_at=timestamp)
        obj.full_clean()
        obj.save()

        self.assertEqual(timestamp, obj.created_at)
        self.assertEqual(timestamp, obj.updated_at)
        # And by transitivity
        self.assertEqual(obj.created_at, obj.updated_at)

        """
        updated_at is not auto updated, created_at stays the same
        """
        obj = TimestampsOpinionated()
        obj.full_clean()
        obj.save()

        original_created_at = obj.created_at
        original_updated_at = obj.updated_at

        obj.save()
        # Get a fresh object
        obj = TimestampsOpinionated.objects.get(id=obj.id)

        self.assertEqual(original_created_at, obj.created_at)
        self.assertEqual(original_updated_at, obj.updated_at)
