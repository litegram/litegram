from __future__ import annotations

import asyncio
import time
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from litestar import Litestar, Request, post
from litestar.testing import TestClient

from litegram import Bot, Dispatcher, F
from litegram.methods import GetMe
from litegram.types import Message, Update, User
from litegram.webhook.litestar_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    webhook_handler,
)
from tests.mocked_bot import MockedBot


class TestSimpleRequestHandler:
    def make_request_data(self, text: str = "test"):
        return {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": text,
            },
        }

    @pytest.mark.anyio
    async def test_reply_into_webhook_text(self, bot: MockedBot):
        dp = Dispatcher()

        @dp.message(F.text == "test")
        def handle_message(msg: Message):
            return msg.answer(text="PASS")

        handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            handle_in_background=False,
        )

        @post("/webhook")
        async def webhook_handler(request: Request) -> Any:
            return await handler(request)

        with TestClient(app=Litestar(route_handlers=[webhook_handler])) as client:
            resp = client.post("/webhook", json=self.make_request_data())
            assert resp.status_code in {200, 201}
            result = resp.json()
            assert result["method"] == "sendMessage"
            assert result["text"] == "PASS"

    @pytest.mark.anyio
    async def test_reply_into_webhook_unhandled(self, bot: MockedBot):
        dp = Dispatcher()

        @dp.message(F.text == "test")
        def handle_message(msg: Message):
            return msg.answer(text="PASS")

        handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            handle_in_background=False,
        )

        @post("/webhook")
        async def webhook_handler(request: Request) -> Any:
            return await handler(request)

        with TestClient(app=Litestar(route_handlers=[webhook_handler])) as client:
            resp = client.post("/webhook", json=self.make_request_data(text="spam"))
            assert resp.status_code in {200, 201}
            assert resp.json() == {}

    @pytest.mark.anyio
    async def test_verify_secret(self, bot: MockedBot):
        dp = Dispatcher()
        handler = SimpleRequestHandler(dispatcher=dp, bot=bot, handle_in_background=False, secret_token="vasya228")

        @post("/webhook")
        async def webhook_handler(request: Request) -> Any:
            return await handler(request)

        with TestClient(app=Litestar(route_handlers=[webhook_handler])) as client:
            resp = client.post("/webhook", json=self.make_request_data())
            assert resp.status_code == 401


class TestOptimizedWebhookHandler:
    def make_request_data(self, text: str = "test"):
        return {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": text,
            },
        }

    @pytest.mark.anyio
    async def test_reply_into_webhook_text(self, bot: MockedBot):
        dp = Dispatcher()

        @dp.message(F.text == "test")
        def handle_message(msg: Message):
            return msg.answer(text="PASS")

        from litestar.di import Provide

        @post("/webhook")
        async def handle(data: Update, request: Request, dispatcher: Dispatcher, bot: Bot) -> Any:
            return await webhook_handler(data=data, request=request, dispatcher=dispatcher, bot=bot)

        app = Litestar(
            route_handlers=[handle],
            dependencies={
                "dispatcher": Provide(lambda: dp, sync_to_thread=False),
                "bot": Provide(lambda: bot, sync_to_thread=False),
            },
        )

        with TestClient(app=app) as client:
            resp = client.post("/webhook", json=self.make_request_data())
            assert resp.status_code in {200, 201}
            result = resp.json()
            assert result["method"] == "sendMessage"
            assert result["text"] == "PASS"


class TestTokenBasedRequestHandler:
    def test_verify_secret(self, bot: MockedBot):
        dispatcher = Dispatcher()
        handler = TokenBasedRequestHandler(dispatcher=dispatcher)
        assert handler.verify_secret("petro328", bot)

    @pytest.mark.anyio
    async def test_close(self):
        dispatcher = Dispatcher()
        handler = TokenBasedRequestHandler(dispatcher=dispatcher)

        bot1 = handler.bots["42:TEST"] = MockedBot(token="42:TEST")
        bot1.add_result_for(GetMe, ok=True, result=User(id=42, is_bot=True, first_name="Test"))
        assert await bot1.get_me()
        assert not bot1.session.closed
        bot2 = handler.bots["1337:TEST"] = MockedBot(token="1337:TEST")
        bot2.add_result_for(GetMe, ok=True, result=User(id=1337, is_bot=True, first_name="Test"))
        assert await bot2.get_me()
        assert not bot2.session.closed

        await handler.close()
        assert bot1.session.closed
        assert bot2.session.closed

    @pytest.mark.anyio
    async def test_resolve_bot(self):
        dispatcher = Dispatcher()
        handler = TokenBasedRequestHandler(dispatcher=dispatcher)

        class FakeRequest:
            def __init__(self, bot_token):
                self.path_parameters = {"bot_token": bot_token}

        bot1 = await handler.resolve_bot(request=FakeRequest(bot_token="42:TEST"))
        assert bot1.id == 42

        bot2 = await handler.resolve_bot(request=FakeRequest(bot_token="1337:TEST"))
        assert bot2.id == 1337

        bot3 = await handler.resolve_bot(request=FakeRequest(bot_token="1337:TEST"))
        assert bot3.id == 1337

        assert bot2 == bot3
        assert len(handler.bots) == 2
