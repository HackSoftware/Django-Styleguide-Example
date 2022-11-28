from typing import Any, Dict, List, Tuple

from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.db import models

from styleguide_example.common.types import DjangoModelType


def model_update(*, instance: DjangoModelType, fields: List[str], data: Dict[str, Any]) -> Tuple[DjangoModelType, bool]:
    """
    Generic update service meant to be reused in local update services

    For example:

    def user_update(*, user: User, data) -> User:
        fields = ['first_name', 'last_name']
        user, has_updated = model_update(instance=user, fields=fields, data=data)

        // Do other actions with the user here

        return user

    Return value: Tuple with the following elements:
        1. The instance we updated
        2. A boolean value representing whether we performed an update or not.
    """
    has_updated = False
    m2m_data = {}
    update_fields = []

    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in data:
            continue

        try:
            model_field = instance._meta.get_field(field)
        except FieldDoesNotExist as exc:
            raise ValidationError(str(exc))

        if isinstance(model_field, models.ManyToManyField):
            has_updated = True
            m2m_data[field] = data[field]

            continue

        if getattr(instance, field) != data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, data[field])

    # Perform an update only if any of the fields were actually changed
    if has_updated:
        instance.full_clean()
        # Update only the fields that are meant to be updated.
        # Django docs reference:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
        instance.save(update_fields=update_fields)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)

    return instance, has_updated
