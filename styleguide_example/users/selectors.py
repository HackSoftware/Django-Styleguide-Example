from typing import Optional

from django.db.models.query import QuerySet

from styleguide_example.api.pagination import CursorPagination, CursorPaginationService

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


def user_list(*, filters=None, pagination: Optional[CursorPagination] = None) -> QuerySet[BaseUser]:
    qs = BaseUser.objects.all()

    if filters is not None:
        qs = BaseUserFilter(filters, qs).qs

    if pagination is not None:
        pagination_service = CursorPaginationService()
        qs = pagination_service.paginate(
            queryset=qs,
            pagination=pagination,
            field="id"
        )

    return qs
