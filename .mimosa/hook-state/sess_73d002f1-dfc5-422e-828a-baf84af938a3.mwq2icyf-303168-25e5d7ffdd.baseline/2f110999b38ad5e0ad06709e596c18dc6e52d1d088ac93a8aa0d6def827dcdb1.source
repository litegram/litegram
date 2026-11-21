from __future__ import annotations

from typing import Any


def resolve_if_needed(value: Any, initial_value: Any) -> Any:
    # To avoid circular imports here is used local import
    from . import MagicFilter

    if not isinstance(value, MagicFilter):
        return value
    return value.resolve(initial_value)
