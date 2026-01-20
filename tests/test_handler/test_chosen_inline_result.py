from __future__ import annotations

from typing import Any

import pytest

from litegram.handlers import ChosenInlineResultHandler
from litegram.types import ChosenInlineResult, User


class TestChosenInlineResultHandler:
    @pytest.mark.anyio
    async def test_attributes_aliases(self):
        event = ChosenInlineResult(
            result_id="chosen",
            from_user=User(id=42, is_bot=False, first_name="Test"),
            query="test",
        )

        class MyHandler(ChosenInlineResultHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user
                assert self.query == self.event.query
                return True

        assert await MyHandler(event)
