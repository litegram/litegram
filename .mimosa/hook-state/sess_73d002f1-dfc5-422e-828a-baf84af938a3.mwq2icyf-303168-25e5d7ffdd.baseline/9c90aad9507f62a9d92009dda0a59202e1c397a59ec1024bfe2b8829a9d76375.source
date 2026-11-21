from __future__ import annotations

from abc import ABC

from litegram.handlers import BaseHandler
from litegram.types import PreCheckoutQuery, User


class PreCheckoutQueryHandler(BaseHandler[PreCheckoutQuery], ABC):
    """
    Base class for pre-checkout handlers
    """

    @property
    def from_user(self) -> User:
        return self.event.from_user
