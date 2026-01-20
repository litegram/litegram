from __future__ import annotations

from .base import TelegramObject


class BackgroundType(TelegramObject):
    """
    This object describes the type of a background. Currently, it can be one of

     - :class:`litegram.types.background_type_fill.BackgroundTypeFill`
     - :class:`litegram.types.background_type_wallpaper.BackgroundTypeWallpaper`
     - :class:`litegram.types.background_type_pattern.BackgroundTypePattern`
     - :class:`litegram.types.background_type_chat_theme.BackgroundTypeChatTheme`

    Source: https://core.telegram.org/bots/api#backgroundtype
    """
