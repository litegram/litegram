from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from litegram import loggers

# Removed TelegramType import
from .base import BaseRequestMiddleware, NextRequestMiddlewareType

if TYPE_CHECKING:
    from litegram.client.bot import Bot
    from litegram.methods import TelegramMethod
    from litegram.methods.base import Response

logger = logging.getLogger(__name__)


class RequestLogging(BaseRequestMiddleware):
    def __init__(self, ignore_methods: list[type[TelegramMethod[Any]]] | None = None):
        """
        Middleware for logging outgoing requests

        :param ignore_methods: methods to ignore in logging middleware
        """
        self.ignore_methods = ignore_methods or []

    async def __call__[TelegramType](
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                "Make request with method=%r by bot id=%d",
                type(method).__name__,
                bot.id,
            )
        return await make_request(bot, method)
