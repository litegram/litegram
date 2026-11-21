from __future__ import annotations

from typing import Any

import pytest

from litegram.handlers import InlineQueryHandler
from litegram.types import InlineQuery, User


class TestCallbackQueryHandler:
    @pytest.mark.anyio
    async def test_attributes_aliases(self):
        event = InlineQuery(
            id="query",
            from_user=User(id=42, is_bot=False, first_name="Test"),
            query="query",
            offset="0",
        )

        class MyHandler(InlineQueryHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user
                assert self.query == self.event.query
                return True

        assert await MyHandler(event)
