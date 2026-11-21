from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import Field

from .base import TelegramObject

if TYPE_CHECKING:
    from .shared_user import SharedUser


class UsersShared(TelegramObject):
    """
    This object contains information about the users whose identifiers were shared with the bot using a :class:`litegram.types.keyboard_button_request_users.KeyboardButtonRequestUsers` button.

    Source: https://core.telegram.org/bots/api#usersshared
    """

    request_id: int
    """Identifier of the request

.. deprecated:: API:7.2
   https://core.telegram.org/bots/api-changelog#march-31-2024"""
    users: list[SharedUser]
    """Information about users shared with the bot"""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(__pydantic__self__, *, request_id: int, users: list[SharedUser], **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(request_id=request_id, users=users, **__pydantic_kwargs)
