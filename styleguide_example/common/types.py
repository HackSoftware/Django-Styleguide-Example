from typing import TypeVar

from django.db import models

# Generic type for a Django model
# Reference: https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
DjangoModelType = TypeVar("DjangoModelType", bound=models.Model)
