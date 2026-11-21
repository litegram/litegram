from __future__ import annotations

import datetime
from typing import Any

import pytest

from litegram.handlers import ChatMemberHandler
from litegram.types import Chat, ChatMemberMember, ChatMemberUpdated, User


class TestChatMemberUpdated:
    @pytest.mark.anyio
    async def test_attributes_aliases(self):
        event = ChatMemberUpdated(
            chat=Chat(id=42, type="private"),
            from_user=User(id=42, is_bot=False, first_name="Test"),
            date=datetime.datetime.now(datetime.UTC),
            old_chat_member=ChatMemberMember(user=User(id=42, is_bot=False, first_name="Test")),
            new_chat_member=ChatMemberMember(user=User(id=42, is_bot=False, first_name="Test")),
        )

        class MyHandler(ChatMemberHandler):
            async def handle(self) -> Any:
                assert self.event == event
                assert self.from_user == self.event.from_user

                return True

        assert await MyHandler(event)
