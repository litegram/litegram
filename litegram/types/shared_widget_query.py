from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .user import User
    from .widget_query_type_union import WidgetQueryTypeUnion


class SharedWidgetQuery(TelegramObject):
    """
    This object represents an incoming query from a forwarded message with a shared widget created by the bot. Use :class:`litegram.methods.answer_widget_query.AnswerWidgetQuery` to answer the query. Each user can send at most 5 queries per 5 seconds to the bot from all its widgets.

    Source: https://core.telegram.org/bots/api#sharedwidgetquery
    """

    id: str
    """Unique identifier for this query"""
    from_user: User = Field(..., alias="from")
    """Sender"""
    type: WidgetQueryTypeUnion
    """Type of the query"""
    data: str
    """Data of the query, 1-64 bytes"""
    widget_id: str
    """Unique identifier of the shared widget, which sent the query"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            id: str,
            from_user: User,
            type: WidgetQueryTypeUnion,
            data: str,
            widget_id: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(id=id, from_user=from_user, type=type, data=data, widget_id=widget_id, **__pydantic_kwargs)
