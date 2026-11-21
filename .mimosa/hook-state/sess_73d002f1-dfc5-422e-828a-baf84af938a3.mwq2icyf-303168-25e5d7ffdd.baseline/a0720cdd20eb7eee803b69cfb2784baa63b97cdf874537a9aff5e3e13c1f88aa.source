from __future__ import annotations

from abc import ABC

from litegram.handlers import BaseHandler
from litegram.types import ChatMemberUpdated, User


class ChatMemberHandler(BaseHandler[ChatMemberUpdated], ABC):
    """
    Base class for chat member updated events
    """

    @property
    def from_user(self) -> User:
        return self.event.from_user
