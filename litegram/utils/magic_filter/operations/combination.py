from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..helper import resolve_if_needed
from .base import BaseOperation

if TYPE_CHECKING:
    from collections.abc import Callable


class CombinationOperation(BaseOperation):
    __slots__ = (
        "right",
        "combinator",
    )

    def __init__(self, right: Any, combinator: Callable[[Any, Any], bool]) -> None:
        self.right = right
        self.combinator = combinator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.combinator(value, resolve_if_needed(self.right, initial_value=initial_value))


class ImportantCombinationOperation(CombinationOperation):
    important = True


class RCombinationOperation(BaseOperation):
    __slots__ = (
        "left",
        "combinator",
    )

    def __init__(self, left: Any, combinator: Callable[[Any, Any], bool]) -> None:
        self.left = left
        self.combinator = combinator

    def resolve(self, value: Any, initial_value: Any) -> Any:
        return self.combinator(resolve_if_needed(self.left, initial_value), value)
