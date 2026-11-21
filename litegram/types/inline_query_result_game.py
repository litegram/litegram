from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import InlineQueryResultType
from .inline_query_result import InlineQueryResult

if TYPE_CHECKING:
    from .inline_keyboard_markup import InlineKeyboardMarkup


class InlineQueryResultGame(InlineQueryResult):
    """
    Represents a :class:`litegram.types.game.Game`.

    Source: https://core.telegram.org/bots/api#inlinequeryresultgame
    """

    type: Literal[InlineQueryResultType.GAME] = InlineQueryResultType.GAME
    """Type of the result, must be *game*"""
    id: str
    """Unique identifier for this result, 1-64 bytes"""
    game_short_name: str
    """Short name of the game"""
    reply_markup: InlineKeyboardMarkup | None = None
    """*Optional*. `Inline keyboard <https://core.telegram.org/bots/features#inline-keyboards>`_ attached to the message"""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            id: str,
            game_short_name: str,
            type: Literal[InlineQueryResultType.GAME] = InlineQueryResultType.GAME,
            reply_markup: InlineKeyboardMarkup | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, id=id, game_short_name=game_short_name, reply_markup=reply_markup, **__pydantic_kwargs)
