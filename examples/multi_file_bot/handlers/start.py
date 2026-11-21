from __future__ import annotations

from typing import TYPE_CHECKING

from litegram import Router
from litegram.filters import CommandStart

if TYPE_CHECKING:
    from litegram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`litegram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    from_user = message.from_user
    if from_user is None:
        return

    await message.answer(f"Hello, <b>{from_user.full_name}!</b>")
