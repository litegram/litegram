from __future__ import annotations

from litegram.types import TelegramObject


class MaybeInaccessibleMessage(TelegramObject):
    """
    This object describes a message that can be inaccessible to the bot. It can be one of

     - :class:`litegram.types.message.Message`
     - :class:`litegram.types.inaccessible_message.InaccessibleMessage`

    Source: https://core.telegram.org/bots/api#maybeinaccessiblemessage
    """
