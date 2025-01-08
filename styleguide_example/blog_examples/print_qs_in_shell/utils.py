from tabulate import tabulate


def tabulate_qs(queryset, *, fields: list[str] | None = None, exclude: list[str] | None = None) -> str:
    # Make sure the table won't be empty
    if not fields:
        fields = [field.name for field in queryset.model._meta.fields]

    if not exclude:
        exclude = []

    fields = [field for field in fields if field not in exclude]

    return tabulate(
        tabular_data=queryset.values_list(*fields),
        headers=fields,
        tablefmt="github",
    )


def print_qs(queryset, *, fields: list[str] | None = None, exclude: list[str] | None = None) -> None:
    print(tabulate_qs(queryset, fields=fields, exclude=exclude))
