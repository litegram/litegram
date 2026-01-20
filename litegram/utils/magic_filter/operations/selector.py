from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..exceptions import RejectOperations
from ..operations import BaseOperation

if TYPE_CHECKING:
    from .. import MagicFilter


class SelectorOperation(BaseOperation):
    __slots__ = ("inner",)

    def __init__(self, inner: MagicFilter):
        self.inner = inner

    def resolve(self, value: Any, initial_value: Any) -> Any:
        if self.inner.resolve(value):
            return value
        raise RejectOperations()
