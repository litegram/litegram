from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from litegram import Dispatcher
from litegram.types import TelegramObject

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


USER = {"id": 1, "is_bot": False, "first_name": "Test"}
CHAT = {"id": 1, "type": "private"}
WIDGET_QUERY = {"id": "q", "from": USER, "type": {"type": "data"}, "data": "test"}


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("kind", "payload", "user_id", "chat_id"),
    [
        ("guest_message", {"message_id": 1, "date": 1, "chat": CHAT, "from": USER}, 1, 1),
        ("widget_query", {**WIDGET_QUERY, "chat_instance": "chat", "chat": CHAT}, 1, 1),
        ("shared_widget_query", {**WIDGET_QUERY, "widget_id": "widget"}, 1, None),
        ("managed_bot", {"user": USER, "bot": {**USER, "id": 2, "is_bot": True}}, 1, None),
        ("subscription", {"user": USER, "invoice_payload": "invoice", "state": "active"}, 1, None),
        ("stopped_message_generation", {"chat": CHAT, "draft_id": 1}, None, 1),
    ],
)
async def test_new_update_dispatch(
    bot: MockedBot, kind: str, payload: dict[str, Any], user_id: int | None, chat_id: int | None
) -> None:
    dispatcher = Dispatcher(disable_fsm=True)

    @dispatcher.observers[kind]()
    async def handler(event: TelegramObject, event_context: Any) -> TelegramObject:
        assert event_context.user_id == user_id
        assert event_context.chat_id == chat_id
        return event

    assert dispatcher.resolve_used_update_types() == [kind]
    result = await dispatcher.feed_raw_update(bot, {"update_id": 1, kind: payload})
    assert isinstance(result, TelegramObject)
    assert result.bot is bot
