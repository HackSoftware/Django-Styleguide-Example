from django.db import models
from django.utils import timezone


class TimestampsWithAuto(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TimestampsWithAutoAndDefault(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class TimestampsWithDefault(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class TimestampsOpinionated(models.Model):
    """
    We want to have the following behavior:

    1. created_at is set by default, but can be overridden.
    2. updated_at is not set on initial creation (stays None).
    3. The service layer (check `model_update`) takes care of providing value to `updated_at`,
        if there's no value provided by the caller.
    """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)


class SomeDataModel(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
    )
    stored_field = models.JSONField(
        blank=True,
    )
