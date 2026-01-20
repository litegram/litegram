from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

from litegram import Bot
from litegram.client.session.base import BaseSession
from litegram.methods.base import Response

# Removed TelegramType import
from litegram.types import UNSET_PARSE_MODE, ResponseParameters, User

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from litegram.methods import TelegramMethod


class MockedSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.responses: deque[Response[Any]] = deque()
        self.requests: deque[TelegramMethod[Any]] = deque()
        self.closed = True

    def add_result[T](self, response: Response[T]) -> Response[T]:
        self.responses.append(response)  # type: ignore[arg-type]
        return response

    def get_request(self) -> TelegramMethod[Any]:
        return self.requests.pop()

    async def close(self):
        self.closed = True

    async def make_request[T](
        self,
        bot: Bot,
        method: TelegramMethod[T],
        timeout: int | None = UNSET_PARSE_MODE,
    ) -> T:
        self.closed = False
        self.requests.append(method)  # type: ignore[arg-type]
        response: Response[T] = self.responses.pop()  # type: ignore[assignment]
        self.check_response(
            bot=bot,
            method=method,
            status_code=response.error_code,
            content=response.model_dump_json(),
        )
        return response.result  # type: ignore

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes]:  # pragma: no cover
        yield b""


class MockedBot(Bot):
    if TYPE_CHECKING:
        session: MockedSession

    def __init__(self, **kwargs):
        super().__init__(kwargs.pop("token", "42:TEST"), session=MockedSession(), **kwargs)
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="FirstName",
            last_name="LastName",
            username="tbot",
            language_code="ru-RU",
        )

    def add_result_for[T](
        self,
        method: type[TelegramMethod[T]],
        ok: bool,
        result: T = None,
        description: str | None = None,
        error_code: int = 200,
        migrate_to_chat_id: int | None = None,
        retry_after: int | None = None,
    ) -> Response[T]:
        response = Response[T](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)
        return response

    def get_request(self) -> TelegramMethod[Any]:
        return self.session.get_request()
