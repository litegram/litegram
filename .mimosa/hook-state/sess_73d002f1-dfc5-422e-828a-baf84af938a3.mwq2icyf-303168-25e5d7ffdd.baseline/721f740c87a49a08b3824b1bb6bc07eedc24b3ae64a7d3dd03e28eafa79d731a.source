from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

from litegram.methods.base import Request

# Removed TelegramType import

if TYPE_CHECKING:
    from litegram.client.bot import Bot
    from litegram.methods import Response, TelegramMethod


class NextRequestMiddlewareType[TelegramType](Protocol):  # pragma: no cover
    async def __call__(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        pass


class RequestMiddlewareType(Protocol):  # pragma: no cover
    async def __call__[TelegramType](
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        pass


class BaseRequestMiddleware(ABC):
    """
    Generic middleware class
    """

    @abstractmethod
    async def __call__[TelegramType](
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:
        """
        Execute middleware

        :param make_request: Wrapped make_request in middlewares chain
        :param bot: bot for request making
        :param method: Request method (Subclass of :class:`litegram.methods.base.TelegramMethod`)

        :return: :class:`litegram.methods.Response`
        """
