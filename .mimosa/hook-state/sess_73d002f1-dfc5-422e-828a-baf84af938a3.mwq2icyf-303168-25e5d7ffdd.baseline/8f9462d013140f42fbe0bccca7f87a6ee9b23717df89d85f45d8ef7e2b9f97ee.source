from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ..operations import BaseOperation

if TYPE_CHECKING:
    from ..magic import MagicFilter


class ExtractOperation(BaseOperation):
    __slots__ = ("extractor",)

    def __init__(self, extractor: MagicFilter) -> None:
        self.extractor = extractor

    def resolve(self, value: Any, initial_value: Any) -> Any:
        if not isinstance(value, Iterable):
            return None

        return [item for item in value if self.extractor.resolve(item)]
