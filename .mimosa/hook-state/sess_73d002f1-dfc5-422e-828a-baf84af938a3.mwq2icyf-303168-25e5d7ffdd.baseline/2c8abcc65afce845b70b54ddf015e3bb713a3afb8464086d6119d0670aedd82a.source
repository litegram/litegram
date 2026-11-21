from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock

import pytest

from litegram import BaseMiddleware, Dispatcher, F
from litegram.enums import ChatType
from litegram.filters import Command
from litegram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from litegram.types import Chat, Message, TelegramObject, Update, User

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from tests.mocked_bot import MockedBot


class EchoScene(Scene, state="test"):
    @on.message.enter()
    async def greetings(self, message: Message, test_context: str):
        await message.answer(f"Echo mode enabled. Context: {test_context}.")

    @on.message(F.text)
    async def echo(self, message: Message, test_context: str):
        await message.reply(f"Your input: {message.text} and Context: {test_context}.")


class TestMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["test_context"] = "Custom context here"
        return await handler(event, data)


@pytest.mark.anyio
async def test_middleware_data_passed_to_scene(bot: MockedBot):
    """Test that middleware data is correctly passed to the scene when using as_handler()."""
    # Create a dispatcher
    dp = Dispatcher()

    # Register the scene handler with the command filter
    dp.message.register(EchoScene.as_handler(), Command("test"))

    # Register the scene with the registry
    scene_registry = SceneRegistry(dp)
    scene_registry.add(EchoScene)

    # Register the middleware
    dp.message.outer_middleware.register(TestMiddleware())

    # Create a proper message with the command
    chat = Chat(id=123, type=ChatType.PRIVATE)
    user = User(id=456, is_bot=False, first_name="Test User")
    message = Message(message_id=1, date=datetime.now(UTC), from_user=user, chat=chat, text="/test")
    update = Update(message=message, update_id=1)

    # Mock the ScenesManager.enter method
    original_enter = ScenesManager.enter
    ScenesManager.enter = AsyncMock()

    try:
        # Process the update
        await dp.feed_update(bot, update)

        # Verify that ScenesManager.enter was called with the test_context from middleware
        ScenesManager.enter.assert_called_once()
        args, kwargs = ScenesManager.enter.call_args
        assert "test_context" in kwargs
        assert kwargs["test_context"] == "Custom context here"
    finally:
        # Restore the original method
        ScenesManager.enter = original_enter
