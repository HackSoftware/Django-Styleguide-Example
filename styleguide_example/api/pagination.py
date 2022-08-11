from collections import OrderedDict

from typing import Optional, Any

from attrs import define

from django.conf import settings

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response

from styleguide_example.common.utils import trycast


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


@define
class CursorPagination:
    page_size: int
    cursor: Optional[Any] = None
    reverse: bool = False


class CursorPaginationService:
    def __init__(
        self,
        *,
        page_size_query_name=None,
        before_query_name=None,
        after_query_name=None
    ):
        self._page_size_query_name = page_size_query_name or "page_size"
        self._before_query_name = before_query_name or "before"
        self._after_query_name = after_query_name or "after"

    def paginate(self, *, queryset, pagination: CursorPagination, field):
        """
        This is a basic cursor pagination implementation.
        """
        page_size = pagination.page_size
        cursor = pagination.cursor
        reverse = pagination.reverse

        # Cursor pagination always enforces ordering
        if reverse:
            queryset = queryset.order_by(f"{field}")
        else:
            queryset = queryset.order_by(f"-{field}")

        if cursor is None:
            return queryset[:page_size]

        field_value = cursor

        if reverse:
            queryset = queryset.filter(**{f"{field}__gt": field_value})
        else:
            queryset = queryset.filter(**{f"{field}__lt": field_value})

        return queryset[:page_size]

    def build_from_query_params(self, query_params) -> CursorPagination:
        page_size = min(
            trycast(
                query_params.get(self._page_size_query_name, settings.PAGINATION_DEFAULT_PAGE_SIZE),
                int
            ),
            settings.PAGINATION_MAX_PAGE_SIZE
        )

        before = query_params.get(self._before_query_name, None)
        after = query_params.get(self._after_query_name, None)

        cursor = None
        reverse = False

        if after is not None:
            cursor = after
            reverse = True

        if before is not None:
            cursor = before
            reverse = False

        return CursorPagination(page_size=page_size, cursor=cursor, reverse=reverse)
