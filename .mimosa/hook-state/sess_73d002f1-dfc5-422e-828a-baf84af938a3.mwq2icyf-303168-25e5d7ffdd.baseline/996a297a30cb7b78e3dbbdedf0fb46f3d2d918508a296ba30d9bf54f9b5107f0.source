from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramMethod

if TYPE_CHECKING:
    from ..types import ChatIdUnion


class ExportChatInviteLink(TelegramMethod[str]):
    """
    Use this method to generate a new primary invite link for a chat; any previously generated primary link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns the new invite link as *String* on success.

    Source: https://core.telegram.org/bots/api#exportchatinvitelink
    """

    __returning__ = str
    __api_method__ = "exportChatInviteLink"

    chat_id: ChatIdUnion
    """Unique identifier for the target chat or username of the target channel in the format :code:`@username`"""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(__pydantic__self__, *, chat_id: ChatIdUnion, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(chat_id=chat_id, **__pydantic_kwargs)
