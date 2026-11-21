from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class PreparedKeyboardButton(TelegramObject):
    """
    Describes a keyboard button to be used by a user of a Mini App.

    Source: https://core.telegram.org/bots/api#preparedkeyboardbutton
    """

    id: str
    """Unique identifier of the keyboard button"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(__pydantic__self__, *, id: str, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(id=id, **__pydantic_kwargs)
