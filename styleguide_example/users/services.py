from typing import Optional

from styleguide_example.users.models import BaseUser


def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: Optional[str] = None
) -> BaseUser:
    user = BaseUser.objects.create_user(
        email=email,
        is_active=is_active,
        is_admin=is_admin,
        password=password
    )

    return user
