from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from litegram.client.default import Default
from litegram.client.session.httpx import HttpxSession
from litegram.exceptions import TelegramNetworkError
from litegram.methods import TelegramMethod
from litegram.types import InputFile

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock

    from litegram import Bot
    from tests.mocked_bot import MockedBot


class BareInputFile(InputFile):
    async def read(self, bot: Bot):
        yield b""


class TestHttpxSession:
    @pytest.mark.anyio
    async def test_create_client(self):
        session = HttpxSession()
        assert session._client is None
        client = await session.create_client()
        assert session._client is not None
        assert isinstance(client, httpx.AsyncClient)
        await session.close()

    @pytest.mark.anyio
    async def test_create_proxy_client(self):
        # httpx handles proxy via string or Proxy object
        async with HttpxSession(proxy="http://user:password@proxy.url:1080/") as session:
            await session.create_client()
            # In httpx 0.27+, we can't easily check internal proxy config from client
            # but we can check if it was initialized
            assert session._proxy == "http://user:password@proxy.url:1080/"

    @pytest.mark.anyio
    async def test_close_client(self):
        session = HttpxSession()
        await session.create_client()

        with patch("httpx.AsyncClient.aclose", new_callable=AsyncMock) as mocked_close:
            # We need to mock the client because it's already created
            session._client.aclose = mocked_close
            await session.close()
            mocked_close.assert_called_once()

    def test_build_request_data_with_data_only(self, bot: MockedBot):
        class TestMethod(TelegramMethod[bool]):
            __api_method__ = "test"
            __returning__ = bool

            str_: str
            int_: int
            bool_: bool
            unset_: str | Default = Default("parse_mode")
            null_: None
            list_: list[str]
            dict_: dict[str, Any]

        session = HttpxSession()
        data, files = session.build_request_data(
            bot,
            TestMethod(
                str_="value",
                int_=42,
                bool_=True,
                unset_=Default("parse_mode"),
                null_=None,
                list_=["foo"],
                dict_={"bar": "baz"},
            ),
        )

        assert len(data) == 5
        assert data["str_"] == "value"
        assert data["int_"] == "42"
        assert data["bool_"] == "true"
        assert "null_" not in data
        assert len(files) == 0

    def test_build_request_data_with_files(self, bot: MockedBot):
        class TestMethod(TelegramMethod[bool]):
            __api_method__ = "test"
            __returning__ = bool

            key: str
            document: InputFile

        session = HttpxSession()
        data, files = session.build_request_data(
            bot,
            TestMethod(key="value", document=BareInputFile(filename="file.txt")),
        )

        assert len(data) == 2
        assert data["key"] == "value"
        assert data["document"].startswith("attach://")

        assert len(files) == 1
        file_key = data["document"][9:]
        assert file_key in files
        assert files[file_key][0] == "file.txt"

    @pytest.mark.anyio
    async def test_make_request(self, bot: MockedBot, httpx_mock: HTTPXMock):
        httpx_mock.add_response(
            url="https://api.telegram.org/bot42:TEST/method",
            method="POST",
            json={"ok": True, "result": 42},
            status_code=200,
        )

        async with HttpxSession() as session:

            class TestMethod(TelegramMethod[int]):
                __returning__ = int
                __api_method__ = "method"

            call = TestMethod()
            result = await session.make_request(bot, call)
            assert isinstance(result, int)
            assert result == 42

    @pytest.mark.anyio
    async def test_make_request_network_error(self, bot: MockedBot, httpx_mock: HTTPXMock):
        httpx_mock.add_exception(httpx.ReadTimeout("mocked"))

        async with HttpxSession() as session:

            class TestMethod(TelegramMethod[int]):
                __returning__ = int
                __api_method__ = "method"

            with pytest.raises(TelegramNetworkError):
                await session.make_request(bot, TestMethod())

    @pytest.mark.anyio
    async def test_stream_content(self, httpx_mock: HTTPXMock):
        url = "https://www.python.org/static/img/python-logo.png"
        httpx_mock.add_response(
            url=url,
            method="GET",
            content=b"\f" * 10,
            status_code=200,
        )

        async with HttpxSession() as session:
            stream = session.stream_content(
                url,
                timeout=5,
                chunk_size=1,
                raise_for_status=True,
            )
            assert isinstance(stream, AsyncGenerator)

            size = 0
            async for chunk in stream:
                assert isinstance(chunk, bytes)
                assert len(chunk) == 1
                size += len(chunk)
            assert size == 10

    @pytest.mark.anyio
    async def test_context_manager(self):
        session = HttpxSession()
        async with session as ctx:
            assert session == ctx
            assert session._client is not None
        assert session._client.is_closed
