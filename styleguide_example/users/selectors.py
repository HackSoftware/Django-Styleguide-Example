from styleguide_example.users.models import BaseUser


def user_get_login_data(*, user: BaseUser):
    return {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
        'is_superuser': user.is_superuser,
    }
