from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, NoReturn
from unittest.mock import sentinel

from litegram.dispatcher.middlewares.base import BaseMiddleware
from litegram.types import TelegramObject

type NextMiddlewareType[MiddlewareEventType: TelegramObject] = Callable[[MiddlewareEventType, dict[str, Any]], Awaitable[Any]]
type MiddlewareType[MiddlewareEventType: TelegramObject] = (
    BaseMiddleware[MiddlewareEventType]
    | Callable[
        [NextMiddlewareType[MiddlewareEventType], MiddlewareEventType, dict[str, Any]],
        Awaitable[Any],
    ]
)


UNHANDLED = sentinel.UNHANDLED
REJECTED = sentinel.REJECTED


class SkipHandler(Exception):
    pass


class CancelHandler(Exception):
    pass


def skip(message: str | None = None) -> NoReturn:
    """
    Raise an SkipHandler
    """
    raise SkipHandler(message or "Event skipped")
