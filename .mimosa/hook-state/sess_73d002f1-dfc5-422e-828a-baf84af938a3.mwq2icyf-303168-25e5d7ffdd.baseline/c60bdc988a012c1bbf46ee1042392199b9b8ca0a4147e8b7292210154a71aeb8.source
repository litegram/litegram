from __future__ import annotations

from typing import Any

from ..exceptions import RejectOperations
from .base import BaseOperation


class CallOperation(BaseOperation):
    __slots__ = ("args", "kwargs")

    def __init__(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        self.args = args
        self.kwargs = kwargs

    def resolve(self, value: Any, initial_value: Any) -> Any:
        if not callable(value):
            raise RejectOperations(TypeError(f"{value} is not callable"))
        return value(*self.args, **self.kwargs)
