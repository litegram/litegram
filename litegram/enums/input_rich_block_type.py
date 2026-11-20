from __future__ import annotations

from enum import Enum


class InputRichBlockType(str, Enum):
    """
    This object represents the type of a inputrichblock object.

    Source: https://core.telegram.org/bots/api#inputrichblock
    """

    ANCHOR = "anchor"
    ANIMATION = "animation"
    AUDIO = "audio"
    BLOCKQUOTE = "blockquote"
    BUTTONS = "buttons"
    COLLAGE = "collage"
    DETAILS = "details"
    DIVIDER = "divider"
    DOCUMENT = "document"
    EXPANDABLE_BLOCKQUOTE = "expandable_blockquote"
    FOOTER = "footer"
    LIST = "list"
    MAP = "map"
    MATHEMATICAL_EXPRESSION = "mathematical_expression"
    PARAGRAPH = "paragraph"
    PHOTO = "photo"
    PRE = "pre"
    PULLQUOTE = "pullquote"
    HEADING = "heading"
    SLIDESHOW = "slideshow"
    TABLE = "table"
    THINKING = "thinking"
    VIDEO = "video"
    VOICE_NOTE = "voice_note"
