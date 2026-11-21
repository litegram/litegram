from __future__ import annotations

from abc import ABC

from litegram.handlers import BaseHandler
from litegram.types import ShippingQuery, User


class ShippingQueryHandler(BaseHandler[ShippingQuery], ABC):
    """
    Base class for shipping query handlers
    """

    @property
    def from_user(self) -> User:
        return self.event.from_user
