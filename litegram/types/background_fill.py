from __future__ import annotations

from .base import TelegramObject


class BackgroundFill(TelegramObject):
    """
    This object describes the way a background is filled based on the selected colors. Currently, it can be one of

     - :class:`litegram.types.background_fill_solid.BackgroundFillSolid`
     - :class:`litegram.types.background_fill_gradient.BackgroundFillGradient`
     - :class:`litegram.types.background_fill_freeform_gradient.BackgroundFillFreeformGradient`

    Source: https://core.telegram.org/bots/api#backgroundfill
    """
