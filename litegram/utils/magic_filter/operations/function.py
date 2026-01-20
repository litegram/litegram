from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..exceptions import RejectOperations
from ..helper import resolve_if_needed
from .base import BaseOperation

if TYPE_CHECKING:
    from collections.abc import Callable


class FunctionOperation(BaseOperation):
    __slots__ = (
        "function",
        "args",
        "kwargs",
    )

    def __init__(self, function: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def resolve(self, value: Any, initial_value: Any) -> Any:
        try:
            return self.function(
                *(resolve_if_needed(arg, initial_value) for arg in self.args),
                value,
                **{k: resolve_if_needed(v, initial_value) for k, v in self.kwargs.items()},
            )
        except (TypeError, ValueError) as e:
            raise RejectOperations(e) from e


class ImportantFunctionOperation(FunctionOperation):
    important = True
