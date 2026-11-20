from __future__ import annotations

from enum import Enum


class RichTextType(str, Enum):
    """
    This object represents the type of a richtext object.

    Source: https://core.telegram.org/bots/api#richtext
    """

    ANCHOR = "anchor"
    ANCHOR_LINK = "anchor_link"
    BANK_CARD_NUMBER = "bank_card_number"
    BOLD = "bold"
    BOT_COMMAND = "bot_command"
    BUTTON = "button"
    CASHTAG = "cashtag"
    CODE = "code"
    CUSTOM_EMOJI = "custom_emoji"
    DATE_TIME = "date_time"
    EMAIL_ADDRESS = "email_address"
    HASHTAG = "hashtag"
    ITALIC = "italic"
    MARKED = "marked"
    MATHEMATICAL_EXPRESSION = "mathematical_expression"
    MENTION = "mention"
    PHONE_NUMBER = "phone_number"
    REFERENCE = "reference"
    REFERENCE_LINK = "reference_link"
    SPOILER = "spoiler"
    STRIKETHROUGH = "strikethrough"
    SUBSCRIPT = "subscript"
    SUPERSCRIPT = "superscript"
    TEXT_MENTION = "text_mention"
    TON_ADDRESS = "ton_address"
    UNDERLINE = "underline"
    URL = "url"
