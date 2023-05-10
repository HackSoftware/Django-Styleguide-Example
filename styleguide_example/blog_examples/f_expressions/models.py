from django.db import models


class SomeDataModel(models.Model):
    """
    This is an example from this blog post
    - https://www.hacksoft.io/blog/django-jsonfield-incrementation-with-f-expressions
    """

    name = models.CharField(
        max_length=255,
        blank=True,
    )
    stored_field = models.JSONField(
        blank=True,
    )
