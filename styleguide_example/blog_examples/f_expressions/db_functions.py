from django.db.models import CharField, F, IntegerField, JSONField, Value
from django.db.models.expressions import Func
from django.db.models.functions import Cast

"""
An F() object represents the value of a model field, transformed value of a model field, or annotated column.
It makes it possible to refer to model field values and perform database operations using them without actually
having to pull them out of the database into Python memory.
"""


class JSONIncrement(Func):
    function = "jsonb_set"

    def __init__(self, full_path, value=1, **extra):
        field_name, *key_path_parts = full_path.split("__")

        if not field_name:
            raise ValueError("`full_path` can not be blank.")

        if len(key_path_parts) < 1:
            raise ValueError("`full_path` must contain at least one key.")

        key_path = ",".join(key_path_parts)

        new_value_expr = Cast(Cast(F(full_path), IntegerField()) + value, CharField())

        expressions = [F(field_name), Value(f"{{{key_path}}}"), Cast(new_value_expr, JSONField())]

        super().__init__(*expressions, output_field=JSONField(), **extra)
