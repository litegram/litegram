from __future__ import annotations

from typing import TYPE_CHECKING, Any

from litegram.filters.base import Filter
from litegram.utils.magic_filter import AttrDict, MagicFilter

if TYPE_CHECKING:
    from litegram.types import TelegramObject


class MagicData(Filter):
    """
    This filter helps to filter event with contextual data
    """

    __slots__ = ("magic_data",)

    def __init__(self, magic_data: MagicFilter) -> None:
        self.magic_data = magic_data

    async def __call__(self, event: TelegramObject, *args: Any, **kwargs: Any) -> Any:
        return self.magic_data.resolve(
            AttrDict({"event": event, **dict(enumerate(args)), **kwargs}),
        )

    def __str__(self) -> str:
        return self._signature_to_string(
            magic_data=self.magic_data,
        )
