from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import (
    InlineQueryResultUnion,
)
from .base import TelegramMethod


class AnswerGuestQuery(TelegramMethod[bool]):
    """
    Use this method to reply to a received guest message. On success, a :class:`litegram.types.sent_guest_message.SentGuestMessage` object is returned.

    Source: https://core.telegram.org/bots/api#answerguestquery
    """

    __returning__ = bool
    __api_method__ = "answerGuestQuery"

    guest_query_id: str
    """Unique identifier for the query to be answered"""
    result: InlineQueryResultUnion
    """A JSON-serialized object describing the message to be sent"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            guest_query_id: str,
            result: InlineQueryResultUnion,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(guest_query_id=guest_query_id, result=result, **__pydantic_kwargs)
