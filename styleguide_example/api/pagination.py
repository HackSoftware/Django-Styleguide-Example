from collections import OrderedDict
from urllib.parse import parse_qs, urlparse

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.pagination import CursorPagination as _CursorPagination
from rest_framework.response import Response


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

    def get_count(self, queryset) -> int:
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            # We remove the prefetches in order to optimize the queryset
            clone = queryset._clone()  # type: ignore
            return (
                clone.prefetch_related(None)
                .select_related(None)
                .only("pk")
                .values_list("pk")
                .count()
            )
        except (AttributeError, TypeError):
            return len(queryset)

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


class CursorPagination(_CursorPagination):
    page_size = 50  # Return 50 items by default

    def __init__(self, ordering):
        self.ordering: str = ordering or "-created_at"

    def get_ordering(self, request, queryset, view):
        # The DRF CursorPagination expects the ordering as a tuple
        if isinstance(self.ordering, str):
            return (self.ordering,)

        return tuple(self.ordering)

    def _get_cursor(self, url):
        if not url:
            return None

        parsed_params = parse_qs(urlparse(url).query)
        # `parse_qs` values are lists
        cursor_params = parsed_params.get("cursor", [])
        if not cursor_params:
            return None

        return cursor_params[0]

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        next_cursor = self._get_cursor(next_url)

        previous_url = self.get_previous_link()
        previous_cursor = self._get_cursor(previous_url)

        return Response(
            OrderedDict(
                [
                    ("next", next_url),
                    ("next_cursor", next_cursor),
                    ("previous", previous_url),
                    ("previous_cursor", previous_cursor),
                    ("results", data),
                ]
            )
        )
