from __future__ import annotations

from dataclasses import dataclass
from re import Match
from typing import TYPE_CHECKING

from litegram import F

if TYPE_CHECKING:
    from litegram.utils.magic_filter import MagicFilter


@dataclass
class MyObject:
    text: str


class TestMagicFilter:
    def test_operation_as(self):
        magic: MagicFilter = F.text.regexp(r"^(\d+)$").as_("match")

        assert not magic.resolve(MyObject(text="test"))

        result = magic.resolve(MyObject(text="123"))
        assert isinstance(result, dict)
        assert isinstance(result["match"], Match)

    def test_operation_as_not_none(self):
        # Issue: https://github.com/litegram/litegram/issues/1281
        magic = F.cast(int).as_("value")

        result = magic.resolve("0")
        assert result == {"value": 0}

    def test_operation_as_not_none_iterable(self):
        # Issue: https://github.com/litegram/litegram/issues/1281
        magic = F.as_("value")

        result = magic.resolve([])
        assert result is None
