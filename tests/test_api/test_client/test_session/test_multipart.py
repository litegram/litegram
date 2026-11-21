from __future__ import annotations

import asyncio
from email import policy
from email.parser import BytesParser
from typing import TYPE_CHECKING

import httpx
import pytest

from litegram import Bot
from litegram.client.session.httpx import HttpxSession
from litegram.methods import SendDocument
from litegram.types import BufferedInputFile, FSInputFile, InputFile, URLInputFile

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from pathlib import Path


@pytest.mark.anyio
async def test_upload_multipart(tmp_path: Path) -> None:
    path = tmp_path / "empty.txt"
    path.write_bytes(b"")

    async def capture(request: httpx.Request) -> httpx.Response:
        body = await request.aread()
        envelope = f"Content-Type: {request.headers['content-type']}\r\n\r\n".encode()
        message = BytesParser(policy=policy.default).parsebytes(envelope + body)
        parts = {part.get_param("name", header="content-disposition"): part for part in message.iter_parts()}
        assert parts["chat_id"].get_payload(decode=True) == b"42"
        for field, filename, payload in (("document", "sample.txt", b"data"), ("thumbnail", "empty.txt", b"")):
            key = parts[field].get_payload(decode=True).decode().removeprefix("attach://")
            assert parts[key].get_filename() == filename
            assert parts[key].get_content_type() == "text/plain"
            assert parts[key].get_payload(decode=True) == payload
        return httpx.Response(200, json={"ok": True, "result": {"message_id": 1, "date": 1, "chat": {"id": 42, "type": "private"}}})

    session = HttpxSession()
    async with httpx.AsyncClient(transport=httpx.MockTransport(capture)) as client:
        session._client = client
        bot = Bot("42:TEST", session=session)
        result = await bot(SendDocument(chat_id=42, document=BufferedInputFile(b"data", "sample.txt"), thumbnail=FSInputFile(path)))
    assert result.message_id == 1


@pytest.mark.anyio
@pytest.mark.parametrize("cancel", [False, True])
async def test_upload_closes_source_when_interrupted(cancel: bool) -> None:
    started = asyncio.Event()
    closed = asyncio.Event()

    class Source(InputFile):
        async def read(self, bot: Bot) -> AsyncGenerator[bytes]:
            try:
                started.set()
                yield b"first chunk"
                pytest.fail("the transport stopped before asking for the next chunk")
            finally:
                closed.set()

    class InterruptTransport(httpx.AsyncBaseTransport):
        async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
            assert isinstance(request.stream, httpx.AsyncByteStream)
            async for chunk in request.stream:
                if chunk == b"first chunk":
                    if cancel:
                        await asyncio.Future()
                    raise httpx.WriteError("interrupted", request=request)
            pytest.fail("source chunk not received")

    session = HttpxSession()
    async with httpx.AsyncClient(transport=InterruptTransport()) as client:
        session._client = client
        bot = Bot("42:TEST", session=session)
        call = SendDocument(chat_id=42, document=Source(filename="test.bin"))
        task = asyncio.ensure_future(bot(call))
        await asyncio.wait_for(started.wait(), timeout=2)
        if cancel:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        else:
            from litegram.exceptions import TelegramNetworkError

            with pytest.raises(TelegramNetworkError, match="interrupted"):
                await task
    assert closed.is_set()


@pytest.mark.anyio
async def test_url_input_file_closes_download() -> None:
    closed = asyncio.Event()

    class Content(httpx.AsyncByteStream):
        async def __aiter__(self) -> AsyncGenerator[bytes]:
            yield b"first"
            yield b"second"

        async def aclose(self) -> None:
            closed.set()

    def serve(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, stream=Content())

    session = HttpxSession()
    async with httpx.AsyncClient(transport=httpx.MockTransport(serve)) as client:
        session._client = client
        bot = Bot("42:TEST", session=session)
        reader = URLInputFile("https://example.test/file", chunk_size=5).read(bot)
        assert await anext(reader) == b"first"
        await reader.aclose()
        assert closed.is_set()
