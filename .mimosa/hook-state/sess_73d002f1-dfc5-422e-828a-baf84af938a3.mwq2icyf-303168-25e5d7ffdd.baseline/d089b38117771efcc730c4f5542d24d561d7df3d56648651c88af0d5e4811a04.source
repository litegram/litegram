from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from .base import MutableTelegramObject


class ForceReply(MutableTelegramObject):
    """
    Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot's message and tapped 'Reply'). This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to sacrifice `privacy mode <https://core.telegram.org/bots/features#privacy-mode>`_. Not supported in channels and for messages sent on behalf of a user account.

    Source: https://core.telegram.org/bots/api#forcereply
    """

    force_reply: Literal[True] = True
    """Shows reply interface to the user, as if they had manually selected the bot's message and tapped 'Reply'"""
    input_field_placeholder: str | None = None
    """*Optional*. The placeholder to be shown in the input field when the reply is active; 1-64 characters"""
    selective: bool | None = None
    """*Optional*. Use this parameter if you want to force reply from specific users only. Targets: 1) users that are @mentioned in the *text* of the :class:`litegram.types.message.Message` object; 2) if the bot's message is a reply to a message in the same chat and forum topic, sender of the original message."""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            force_reply: Literal[True] = True,
            input_field_placeholder: str | None = None,
            selective: bool | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                force_reply=force_reply,
                input_field_placeholder=input_field_placeholder,
                selective=selective,
                **__pydantic_kwargs,
            )
