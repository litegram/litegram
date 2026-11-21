"""End-to-end upload over a real socket: chunked transfer + multipart body.

These tests bind an ephemeral localhost port and run the full client stack
(HttpxSession -> httpx -> socket), not a mocked transport, so they capture
the raw wire bytes exactly as an HTTP server would see them.
"""

from __future__ import annotations

import threading
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TYPE_CHECKING, Any

import pytest

from litegram import Bot
from litegram.client.session.httpx import HttpxSession
from litegram.client.telegram import TelegramAPIServer
from litegram.methods import SendDocument
from litegram.types import BufferedInputFile, Message

if TYPE_CHECKING:
    from collections.abc import Generator


class _Capture:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.body = b""
        self.path = ""
        self.received = threading.Event()


class _Handler(BaseHTTPRequestHandler):
    capture: _Capture
    protocol_version = "HTTP/1.1"

    def do_POST(self) -> None:  # noqa: N802 — BaseHTTPRequestHandler naming
        self.capture.body = self._read_body()
        self.capture.headers = {k.lower(): v for k, v in self.headers.items()}
        self.capture.path = self.path
        self.capture.received.set()
        response = b'{"ok":true,"result":{"message_id":1,"date":1,"chat":{"id":42,"type":"private"}}}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def _read_body(self) -> bytes:
        """Read a request body, transparently decoding chunked transfer."""
        length = self.headers.get("Content-Length")
        if length is not None:
            return self.rfile.read(int(length))
        body = bytearray()
        while True:
            size_line = self.rfile.readline().strip()
            size = int(size_line.split(b";")[0], 16)
            if size == 0:
                self.rfile.readline()  # trailing CRLF after the last chunk
                break
            body.extend(self.rfile.read(size))
            self.rfile.readline()  # CRLF after each chunk
        return bytes(body)

    def log_message(self, *_args: Any) -> None:  # pragma: no cover
        pass


@pytest.fixture()
def capture_server() -> Generator[tuple[_Capture, int], None, None]:
    capture = _Capture()
    handler = type("BoundHandler", (_Handler,), {"capture": capture})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield capture, server.server_address[1]
    finally:
        server.shutdown()
        server.server_close()


def _session_on_port(port: int) -> HttpxSession:
    session = HttpxSession()
    session.api = TelegramAPIServer.from_base(f"http://127.0.0.1:{port}")
    return session


@pytest.mark.anyio
async def test_upload_over_real_socket_is_well_formed(capture_server: Any):
    capture, port = capture_server
    bot = Bot("42:TEST", session=_session_on_port(port))

    result = await bot(
        SendDocument(
            chat_id=42,
            document=BufferedInputFile(b"file payload", "sample.txt"),
            caption="caption <safe>",
        )
    )
    assert isinstance(result, Message)
    assert result.message_id == 1
    assert capture.received.is_set()

    assert capture.path == "/bot42:TEST/sendDocument"
    # HTTPX streams an async iterable with chunked transfer encoding.
    assert capture.headers.get("transfer-encoding") == "chunked"
    content_type = capture.headers["content-type"]
    assert content_type.startswith("multipart/form-data; boundary=")
    boundary = content_type.split("boundary=", maxsplit=1)[1]

    envelope = f"Content-Type: {content_type}\r\n\r\n".encode()
    message = BytesParser(policy=policy.default).parsebytes(envelope + capture.body)
    parts = {part.get_param("name", header="content-disposition"): part for part in message.iter_parts()}
    assert parts["chat_id"].get_payload(decode=True) == b"42"
    assert parts["caption"].get_payload(decode=True) == b"caption <safe>"
    key = parts["document"].get_payload(decode=True).decode().removeprefix("attach://")
    assert parts[key].get_filename() == "sample.txt"
    assert parts[key].get_payload(decode=True) == b"file payload"
    # The body ends with the multipart closing delimiter.
    assert capture.body.endswith(f"--{boundary}--\r\n".encode())


@pytest.mark.anyio
async def test_form_only_request_over_real_socket(capture_server: Any):
    capture, port = capture_server
    bot = Bot("42:TEST", session=_session_on_port(port))

    await bot(SendDocument(chat_id=42, document="file-id-string"))

    # A request without attachments keeps the classic form-encoded path.
    assert capture.headers.get("transfer-encoding") is None
    assert capture.headers.get("content-type") == "application/x-www-form-urlencoded"
