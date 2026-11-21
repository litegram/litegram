from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from litegram import Dispatcher
from litegram.filters.base import Filter

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class InjectingFilter(Filter):
    """Filter that injects data into the handler context."""

    def __init__(self, marker: str) -> None:
        self.marker = marker

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        return {"injected": self.marker}


def make_filter(marker: str) -> InjectingFilter:
    return InjectingFilter(marker)


class TestHandlerDataIsolation:
    @pytest.mark.anyio
    async def test_skipped_handler_data_does_not_leak(self, bot: MockedBot):
        dispatcher = Dispatcher()
        seen: list[dict[str, Any]] = []

        @dispatcher.message(make_filter("first"))
        async def first(message: Any) -> Any:
            from litegram.dispatcher.event.bases import SkipHandler

            raise SkipHandler()

        @dispatcher.message()
        async def second(message: Any, **kwargs: Any) -> Any:
            seen.append(dict(kwargs))
            return "handled"

        result = await dispatcher.feed_raw_update(
            bot, {"update_id": 1, "message": {"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}
        )
        assert result == "handled"
        assert seen, "second handler must run"
        assert "injected" not in seen[0], "first handler's filter data leaked into the second handler"

    @pytest.mark.anyio
    async def test_matching_handler_sees_its_filter_data(self, bot: MockedBot):
        dispatcher = Dispatcher()
        seen: list[dict[str, Any]] = []

        @dispatcher.message(make_filter("matched"))
        async def handler(message: Any, **kwargs: Any) -> Any:
            seen.append(dict(kwargs))
            return "handled"

        result = await dispatcher.feed_raw_update(
            bot, {"update_id": 1, "message": {"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}
        )
        assert result == "handled"
        assert seen[0]["injected"] == "matched"

    @pytest.mark.anyio
    async def test_outer_middleware_sees_isolated_context(self, bot: MockedBot):
        dispatcher = Dispatcher()
        observed: list[Any] = []

        async def spy(handler: Any, event: Any, data: dict[str, Any]) -> Any:
            observed.append(data.get("injected"))
            return await handler(event, data)

        @dispatcher.message(make_filter("first"))
        async def skipped(message: Any) -> Any:
            from litegram.dispatcher.event.bases import SkipHandler

            raise SkipHandler()

        @dispatcher.message()
        async def handler(message: Any) -> Any:
            return "handled"

        dispatcher.message.outer_middleware(spy)
        result = await dispatcher.feed_raw_update(
            bot, {"update_id": 1, "message": {"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}
        )
        assert result == "handled"
        assert observed == [None], "outer middlewares must not see a skipped handler's filter data"
