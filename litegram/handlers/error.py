from __future__ import annotations

from abc import ABC

from litegram.handlers.base import BaseHandler
from litegram.types import ErrorEvent


class ErrorHandler(BaseHandler[ErrorEvent | Exception], ABC):
    """
    Base class for errors handlers
    """

    @property
    def exception(self) -> Exception:
        return self.event.exception if isinstance(self.event, ErrorEvent) else self.event

    @property
    def exception_name(self) -> str:
        return type(self.exception).__name__

    @property
    def exception_message(self) -> str:
        return str(self.exception)
