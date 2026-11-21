from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from litegram import Dispatcher
from litegram.types import Message, Update

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


def _update() -> Update:
    return Update(update_id=1, message={"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}})


@pytest.mark.anyio
async def test_start_polling_shutdown_drains_handlers(bot: MockedBot):
    dispatcher = Dispatcher()
    started = asyncio.Event()
    release = asyncio.Event()
    processed: list[int] = []

    async def handler(message: Message):
        started.set()
        await release.wait()
        processed.append(message.message_id)

    dispatcher.message.register(handler)

    async def _mock_updates(*_, **__):
        yield _update()

    with patch.object(Dispatcher, "_listen_updates", _mock_updates):
        polling_task = asyncio.ensure_future(
            dispatcher.start_polling(bot, polling_timeout=1, handle_signals=False, drain_timeout=5)
        )
        await asyncio.wait_for(started.wait(), timeout=5)
        release.set()
        await asyncio.wait_for(polling_task, timeout=10)

    assert processed == [1]
    assert not dispatcher._handle_update_tasks
    await dispatcher.fsm.storage.close()


@pytest.mark.anyio
async def test_start_polling_cancels_stuck_handler_after_drain_timeout(bot: MockedBot):
    dispatcher = Dispatcher()
    started = asyncio.Event()
    cancelled = asyncio.Event()
    processed: list[int] = []

    async def handler(message: Message):
        started.set()
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            cancelled.set()
            raise
        processed.append(message.message_id)

    dispatcher.message.register(handler)

    async def _mock_updates(*_, **__):
        yield _update()

    with patch.object(Dispatcher, "_listen_updates", _mock_updates):
        polling_task = asyncio.ensure_future(
            dispatcher.start_polling(bot, polling_timeout=1, handle_signals=False, drain_timeout=0.2)
        )
        await asyncio.wait_for(started.wait(), timeout=5)
        await asyncio.wait_for(cancelled.wait(), timeout=10)
        await asyncio.wait_for(polling_task, timeout=10)

    assert processed == []
    assert not dispatcher._handle_update_tasks
    await dispatcher.fsm.storage.close()
