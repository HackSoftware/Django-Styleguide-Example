from collections import OrderedDict
from typing import Optional, Sequence, Tuple, Type, Union
from urllib.parse import parse_qs, urlparse

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.pagination import BasePagination
from rest_framework.pagination import CursorPagination as _CursorPagination
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class _TurnOffPaginationSerializer(serializers.Serializer):
    paginate = serializers.BooleanField(default=True)


def turn_off_pagination(data):
    serializer = _TurnOffPaginationSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    return serializer.validated_data["paginate"]


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_count(self, queryset: Union[QuerySet, Sequence]) -> int:
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
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class CursorPagination(_CursorPagination):
    page_size = 50  # Return 50 items by default

    def __init__(self, ordering: Optional[str]):
        self.ordering: str = ordering or "-created_at"

    def get_ordering(
        self, request: Request, queryset: QuerySet, view: APIView
    ) -> Tuple[str]:
        # The DRF CursorPagination expects the ordering as a tuple
        if isinstance(self.ordering, str):
            return (self.ordering,)

        return tuple(self.ordering)

    def _get_cursor(self, url: Optional[str]) -> Optional[str]:
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


def _init_pagination_class(
    pagination_class: Type[BasePagination],
    ordering: Optional[str],
) -> BasePagination:
    if isinstance(pagination_class, CursorPagination):
        return pagination_class(ordering=ordering)

    return pagination_class()


def response_paginate(
    *,
    pagination_class: Type[BasePagination],
    serializer_class: Type[serializers.Serializer],
    queryset: QuerySet,
    request: Request,
    view: APIView,
    ordering: Optional[str] = "-created_at"
) -> Response:
    paginate = turn_off_pagination(data=request.GET)

    if not paginate:
        data = serializer_class(queryset, many=True).data

        return Response(data=data)

    paginator = _init_pagination_class(pagination_class, ordering)

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)
