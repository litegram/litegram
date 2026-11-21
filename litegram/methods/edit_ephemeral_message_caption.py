from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import (
    ChatIdUnion,
    InlineKeyboardMarkup,
    MessageEntity,
)
from .base import TelegramMethod


class EditEphemeralMessageCaption(TelegramMethod[bool]):
    """
    Use this method to edit the caption of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, :code:`True` is returned.

    Source: https://core.telegram.org/bots/api#editephemeralmessagecaption
    """

    __returning__ = bool
    __api_method__ = "editEphemeralMessageCaption"

    chat_id: ChatIdUnion
    """Unique identifier for the target chat or username of the target supergroup in the format :code:`@username`"""
    receiver_user_id: int
    """Identifier of the user who received the message"""
    ephemeral_message_id: int
    """Identifier of the ephemeral message to edit"""
    caption: str | None = None
    """New caption of the message, 0-1024 characters after entities parsing"""
    parse_mode: str | None = None
    """Mode for parsing entities in the message caption. See `formatting options <https://core.telegram.org/bots/api#formatting-options>`_ for more details."""
    caption_entities: list[MessageEntity] | None = None
    """A JSON-serialized list of special entities that appear in the caption, which can be specified instead of *parse_mode*"""
    show_caption_above_media: bool | None = None
    """Pass :code:`True` if the caption must be shown above the message media. Supported only for animation, photo and video messages."""
    reply_markup: InlineKeyboardMarkup | None = None
    """A JSON-serialized object for an `inline keyboard <https://core.telegram.org/bots/features#inline-keyboards>`_"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            chat_id: ChatIdUnion,
            receiver_user_id: int,
            ephemeral_message_id: int,
            caption: str | None = None,
            parse_mode: str | None = None,
            caption_entities: list[MessageEntity] | None = None,
            show_caption_above_media: bool | None = None,
            reply_markup: InlineKeyboardMarkup | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                chat_id=chat_id,
                receiver_user_id=receiver_user_id,
                ephemeral_message_id=ephemeral_message_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                show_caption_above_media=show_caption_above_media,
                reply_markup=reply_markup,
                **__pydantic_kwargs,
            )
