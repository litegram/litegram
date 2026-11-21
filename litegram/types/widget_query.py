from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User
    from .widget_query_type_union import WidgetQueryTypeUnion


class WidgetQuery(TelegramObject):
    """
    This object represents an incoming query from a widget in a message sent by the bot or via the bot. Use :class:`litegram.methods.answer_widget_query.AnswerWidgetQuery` to answer the query. Each user can send at most 5 queries per 5 seconds to the bot from all its widgets.

    Source: https://core.telegram.org/bots/api#widgetquery
    """

    id: str
    """Unique identifier for this query"""
    from_user: User = Field(..., alias="from")
    """Sender"""
    chat: Chat | None = None
    """*Optional*. Chat with the message containing the widget; omitted if the widget is in an inline message"""
    message_id: int | None = None
    """*Optional*. Identifier of the message containing the widget; omitted if the widget is in an inline message"""
    inline_message_id: str | None = None
    """*Optional*. Identifier of the inline message containing the widget"""
    chat_instance: str
    """Global identifier, uniquely corresponding to the chat to which the message with the widget was sent"""
    chat_type: str | None = None
    """*Optional*. For widgets in inline messages, type of the chat to which the message was sent. Can be either 'sender' for a private chat with the inline query sender, 'private', 'group', 'supergroup', or 'channel'."""
    type: WidgetQueryTypeUnion
    """Type of the query"""
    data: str
    """Data of the query, 1-64 bytes"""
    widget_id: str | None = None
    """*Optional*. Unique identifier of the shared widget, which sent the query; omitted if the widget isn't shared"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            id: str,
            from_user: User,
            chat_instance: str,
            type: WidgetQueryTypeUnion,
            data: str,
            chat: Chat | None = None,
            message_id: int | None = None,
            inline_message_id: str | None = None,
            chat_type: str | None = None,
            widget_id: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                id=id,
                from_user=from_user,
                chat_instance=chat_instance,
                type=type,
                data=data,
                chat=chat,
                message_id=message_id,
                inline_message_id=inline_message_id,
                chat_type=chat_type,
                widget_id=widget_id,
                **__pydantic_kwargs,
            )
