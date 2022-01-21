from typing import TypeVar

from django.db import transaction

T = TypeVar('T')


@transaction.atomic
def generic_update(*, instance: T, **fields_to_update) -> T:
    """
    Generic update service meant to be reused in local update services

    For example:

    def user_update(*, user: User, **fields_to_update) -> User:
        user = generic_update(instance=user, **fields_to_update)

        // Do other actions with the user here

        return user
    """
    # If the passed instance is `None` - do nothing.
    if instance is None:
        return instance

    # If there's nothing to update - do not perform unnecessary actions.
    if not fields_to_update:
        return instance

    for attr, value in fields_to_update.items():
        setattr(instance, attr, value)

    instance.full_clean()
    # Update only the fields that are meant to be updated.
    # Django docs reference: https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
    update_fields = list(fields_to_update.keys())
    instance.save(update_fields=update_fields)

    return instance
