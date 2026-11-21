from __future__ import annotations

from typing import TYPE_CHECKING, Any

from litegram.types import TelegramObject


class BotShortDescription(TelegramObject):
    """
    This object represents the bot's short description.

    Source: https://core.telegram.org/bots/api#botshortdescription
    """

    short_description: str
    """The bot's short description"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(__pydantic__self__, *, short_description: str, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(short_description=short_description, **__pydantic_kwargs)
