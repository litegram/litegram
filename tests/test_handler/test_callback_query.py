from __future__ import annotations

from typing import Any

import pytest

from litegram.handlers import CallbackQueryHandler
from litegram.types import CallbackQuery, User


class TestCallbackQueryHandler:
    @pytest.mark.anyio
    async def test_attributes_aliases(self):
        event = CallbackQuery(
            id="chosen",
            from_user=User(id=42, is_bot=False, first_name="Test"),
            data="test",
            chat_instance="test",
        )

        class MyHandler(CallbackQueryHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user
                assert self.callback_data == self.event.data
                assert self.message == self.message
                return True

        assert await MyHandler(event)
