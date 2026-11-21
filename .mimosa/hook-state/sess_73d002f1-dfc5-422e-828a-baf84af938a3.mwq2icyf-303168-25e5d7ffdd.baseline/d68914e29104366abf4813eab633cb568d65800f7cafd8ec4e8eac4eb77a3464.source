from __future__ import annotations

from abc import ABC

from litegram.handlers import BaseHandler
from litegram.types import Poll, PollOption


class PollHandler(BaseHandler[Poll], ABC):
    """
    Base class for poll handlers
    """

    @property
    def question(self) -> str:
        return self.event.question

    @property
    def options(self) -> list[PollOption]:
        return self.event.options
