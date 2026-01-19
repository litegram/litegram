from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Self, cast

import httpx

from litegram.__meta__ import __version__
from litegram.exceptions import TelegramNetworkError
from litegram.methods.base import Request

# Removed TelegramType import as we'll use PEP 695 type parameters
from .base import BaseSession

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from litegram.client.bot import Bot
    from litegram.methods import TelegramMethod
    from litegram.types import InputFile


class HttpxSession(BaseSession):
    def __init__(self, proxy: str | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._proxy = proxy
        self._client: httpx.AsyncClient | None = None

    async def create_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                proxy=self._proxy,
                headers={"User-Agent": f"litegram/{__version__}"},
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()

    def build_request_data[TelegramType](
        self, bot: Bot, method: TelegramMethod[TelegramType]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        data = {}
        files = {}
        input_files: dict[str, InputFile] = {}
        for key, value in method.model_dump(warnings=False).items():
            value = self.prepare_value(value, bot=bot, files=input_files)
            if value is not None:
                data[key] = value
        for key, value in input_files.items():
            files[key] = (value.filename or key, value.read(bot))
        return data, files

    async def make_request[TelegramType](
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: int | None = None,
    ) -> TelegramType:
        client = await self.create_client()
        url = self.api.api_url(token=bot.token, method=method.__api_method__)
        data, files = self.build_request_data(bot=bot, method=method)

        try:
            response = await client.post(
                url,
                data=data,
                files=files,
                timeout=self.timeout if timeout is None else timeout,
            )
            raw_result = response.text
        except httpx.TimeoutException as e:
            raise TelegramNetworkError(method=method, message="Request timeout error") from e
        except httpx.RequestError as e:
            raise TelegramNetworkError(method=method, message=f"{type(e).__name__}: {e}") from e

        checked_response = self.check_response(
            bot=bot,
            method=method,
            status_code=response.status_code,
            content=raw_result,
        )
        return cast("TelegramType", checked_response.result)

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes]:
        client = await self.create_client()
        async with client.stream("GET", url, headers=headers, timeout=timeout, follow_redirects=True) as response:
            if raise_for_status:
                response.raise_for_status()
            async for chunk in response.aiter_bytes(chunk_size):
                yield chunk

    async def __aenter__(self) -> Self:
        await self.create_client()
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: Any) -> None:
        await self.close()
