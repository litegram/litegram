from __future__ import annotations

import pytest

from litegram import F
from litegram.filters import MagicData
from litegram.types import Update
from litegram.utils.magic_filter import AttrDict


class TestMagicDataFilter:
    @pytest.mark.anyio
    async def test_call(self):
        called = False

        def check(value):
            nonlocal called
            called = True

            assert isinstance(value, AttrDict)
            assert value[0] == "foo"
            assert value[1] == "bar"
            assert value["spam"] is True
            assert value.spam is True
            return value

        f = MagicData(magic_data=F.func(check).as_("test"))
        result = await f(Update(update_id=123), "foo", "bar", spam=True)

        assert called
        assert isinstance(result, dict)
        assert result["test"]

    def test_str(self):
        f = MagicData(magic_data=F.event.text == "test")
        assert str(f).startswith("MagicData(magic_data=")
