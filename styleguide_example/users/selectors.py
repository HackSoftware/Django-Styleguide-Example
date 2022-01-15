from django.db.models.query import QuerySet

from styleguide_example.users.models import BaseUser
from styleguide_example.users.filters import BaseUserFilter


def user_get_login_data(*, user: BaseUser):
    return {
        'id': user.id,
        'email': user.email,
        'is_active': user.is_active,
        'is_admin': user.is_admin,
        'is_superuser': user.is_superuser,
    }


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs
