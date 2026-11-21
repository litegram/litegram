from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram import Dispatcher
from litegram.dispatcher.event.handler import CallableObject
from litegram.fsm.scene import SceneRegistry
from litegram.fsm.state import State, StatesGroup
from litegram.fsm.strategy import FSMStrategy
from litegram.handlers import ErrorHandler
from litegram.types import Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


@pytest.mark.anyio
async def test_async_callable_is_awaited() -> None:
    class Callback:
        async def __call__(self, result: str) -> str:
            return result

    assert await CallableObject(Callback()).call(result="handled") == "handled"


def test_nested_state_names_and_membership() -> None:
    class Root(StatesGroup):
        class Child(StatesGroup):
            class Grandchild(StatesGroup):
                class Leaf(StatesGroup):
                    active = State()

    leaf = Root.Child.Grandchild.Leaf
    assert leaf in Root
    assert leaf.active.state == "Root.Child.Grandchild.Leaf:active"
    assert leaf.active.state in leaf


@pytest.mark.parametrize(("strategy", "thread_id"), [(FSMStrategy.CHAT, None), (FSMStrategy.CHAT_TOPIC, 7)])
def test_chat_only_fsm_context(bot: MockedBot, strategy: FSMStrategy, thread_id: int | None) -> None:
    context = Dispatcher(fsm_strategy=strategy).fsm.resolve_context(bot, chat_id=-100, user_id=None, thread_id=7)
    assert context is not None
    assert (context.key.chat_id, context.key.user_id, context.key.thread_id) == (-100, -100, thread_id)


@pytest.mark.anyio
async def test_error_handler_and_scene_registry_without_fsm(bot: MockedBot) -> None:
    dispatcher = Dispatcher(disable_fsm=True)
    SceneRegistry(dispatcher)

    @dispatcher.message()
    async def fail(message: Message) -> None:
        raise ValueError("handler failed")

    @dispatcher.errors()
    class Handler(ErrorHandler):
        async def handle(self) -> tuple[str, str]:
            return self.exception_name, self.exception_message

    result = await dispatcher.feed_raw_update(
        bot, {"update_id": 1, "message": {"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}
    )
    assert result == ("ValueError", "handler failed")
