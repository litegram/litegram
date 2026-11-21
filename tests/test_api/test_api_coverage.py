from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock

import pytest

from litegram import Dispatcher, methods
from litegram.fsm.scene import SceneRegistry
from litegram.fsm.storage.memory import StorageKey
from litegram.fsm.storage.mongo import MongoStorage
from litegram.fsm.storage.pymongo import PyMongoStorage
from litegram.methods import GetMe
from litegram.types import Update
from litegram.utils.chat_action import ChatActionSender
from litegram.utils.web_app import safe_parse_webapp_init_data

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestFrameworkEdgeCoverage:
    def test_update_hash(self):
        assert hash(Update(update_id=42)) == hash(Update(update_id=42))
        assert hash(Update(update_id=42)) != hash(Update(update_id=1))

    def test_methods_namespace_skips_non_pydantic_entries(self):
        original_all = methods.__all__
        methods.__all__ = (*methods.__all__, "_CoverageDummy")
        methods.__dict__["_CoverageDummy"] = object()
        try:
            methods._rebuild_models()
        finally:
            methods.__all__ = original_all
            methods.__dict__.pop("_CoverageDummy", None)

    @pytest.mark.anyio
    async def test_webhook_result_error_returns_empty_dict(self, bot: MockedBot):
        dispatcher = Dispatcher()
        dispatcher._feed_webhook_update = AsyncMock(side_effect=RuntimeError("handler failed"))
        assert await dispatcher.feed_webhook_update(bot, Update(update_id=42)) == {}

    @pytest.mark.anyio
    async def test_scene_middleware_without_state(self):
        handler = AsyncMock(return_value="handled")
        result = await SceneRegistry(Dispatcher())._middleware(handler, event=object(), data={})
        assert result == "handled"


class TestMongoUpdateEmptyResult:
    @pytest.mark.anyio
    async def test_pymongo_update_result_none(self):
        client = MagicMock()
        collection = MagicMock()
        collection.find_one_and_update = AsyncMock(return_value=None)
        client.__getitem__.return_value.__getitem__.return_value = collection
        storage = PyMongoStorage(client=client)
        key = StorageKey(chat_id=1, user_id=2, bot_id=3)
        assert await storage.update_data(key, {"state": "new"}) == {}

    @pytest.mark.anyio
    async def test_mongo_update_result_none(self):
        client = MagicMock()
        collection = MagicMock()
        collection.find_one_and_update = AsyncMock(return_value=None)
        client.__getitem__.return_value.__getitem__.return_value = collection
        storage = MongoStorage(client=client)
        key = StorageKey(chat_id=1, user_id=2, bot_id=3)
        assert await storage.update_data(key, {"state": "new"}) == {}


class TestWebAppTimeout:
    VALID = (
        "auth_date=1650385342"
        "&user=%7B%22id%22%3A42%2C%22first_name%22%3A%22Test%22%7D"
        "&query_id=test"
        "&hash=46d2ea5e32911ec8d30999b56247654460c0d20949b6277af519e76271182803"
    )

    def test_valid_data_without_timeout(self):
        result = safe_parse_webapp_init_data("42:TEST", self.VALID)
        assert result.user is not None
        assert result.user.id == 42

    def test_old_data_rejected_with_timeout(self):
        with pytest.raises(ValueError, match="too old"):
            safe_parse_webapp_init_data("42:TEST", self.VALID, auth_date_timeout=60)


class TestChatActionWorkerErrors:
    @pytest.mark.anyio
    async def test_worker_error_is_collected(self, bot: MockedBot):
        bot.send_chat_action = AsyncMock(side_effect=RuntimeError("send failed"))
        sender = ChatActionSender(bot=bot, chat_id=42, interval=0.01, initial_sleep=0)
        await sender._run()
        await asyncio.sleep(0.05)
        await sender._stop()
        assert isinstance(sender._worker_error, RuntimeError)
        assert sender._task is None

    @pytest.mark.anyio
    async def test_worker_cancellation_is_reraised(self, bot: MockedBot):
        bot.send_chat_action = AsyncMock(side_effect=asyncio.CancelledError)
        sender = ChatActionSender(bot=bot, chat_id=42, initial_sleep=0)
        with pytest.raises(asyncio.CancelledError):
            await sender._worker()
        assert sender._closed_event.is_set()
