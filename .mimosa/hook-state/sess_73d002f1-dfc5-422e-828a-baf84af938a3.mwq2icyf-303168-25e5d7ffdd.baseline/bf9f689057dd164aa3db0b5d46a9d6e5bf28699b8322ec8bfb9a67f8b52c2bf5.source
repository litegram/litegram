from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

import pytest

from litegram.client.session.middlewares.request_logging import RequestLogging
from litegram.methods import GetMe, SendMessage
from litegram.types import Chat, Message, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestRequestLogging:
    @pytest.mark.anyio
    async def test_use_middleware(self, bot: MockedBot, caplog):
        caplog.set_level(logging.INFO)
        bot.session.middleware(RequestLogging())

        bot.add_result_for(GetMe, ok=True, result=User(id=42, is_bot=True, first_name="Test"))
        assert await bot.get_me()
        assert "Make request with method='GetMe' by bot id=42" in caplog.text

    @pytest.mark.anyio
    async def test_ignore_methods(self, bot: MockedBot, caplog):
        caplog.set_level(logging.INFO)
        bot.session.middleware(RequestLogging(ignore_methods=[GetMe]))

        bot.add_result_for(GetMe, ok=True, result=User(id=42, is_bot=True, first_name="Test"))
        assert await bot.get_me()
        assert "Make request with method='GetMe' by bot id=42" not in caplog.text

        bot.add_result_for(
            SendMessage,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                text="test",
                chat=Chat(id=42, type="private"),
            ),
        )
        assert await bot.send_message(chat_id=1, text="Test")
        assert "Make request with method='SendMessage' by bot id=42" in caplog.text
