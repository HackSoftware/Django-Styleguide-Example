from django.db import models

"""
This is a basic model used to illustrate
JSON field increment with f expressions
"""


class SomeDataModel(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
    )
    stored_field = models.JSONField(
        blank=True,
    )
