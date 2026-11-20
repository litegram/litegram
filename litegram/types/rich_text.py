from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class RichText(TelegramObject):
    """
    This object represents a rich formatted text. Currently, it can be either a String for plain text, an Array of :class:`litegram.types.rich_text.RichText`, or any of the following types:

     - :class:`litegram.types.rich_text_bold.RichTextBold`
     - :class:`litegram.types.rich_text_italic.RichTextItalic`
     - :class:`litegram.types.rich_text_underline.RichTextUnderline`
     - :class:`litegram.types.rich_text_strikethrough.RichTextStrikethrough`
     - :class:`litegram.types.rich_text_spoiler.RichTextSpoiler`
     - :class:`litegram.types.rich_text_date_time.RichTextDateTime`
     - :class:`litegram.types.rich_text_text_mention.RichTextTextMention`
     - :class:`litegram.types.rich_text_subscript.RichTextSubscript`
     - :class:`litegram.types.rich_text_superscript.RichTextSuperscript`
     - :class:`litegram.types.rich_text_marked.RichTextMarked`
     - :class:`litegram.types.rich_text_code.RichTextCode`
     - :class:`litegram.types.rich_text_custom_emoji.RichTextCustomEmoji`
     - :class:`litegram.types.rich_text_mathematical_expression.RichTextMathematicalExpression`
     - :class:`litegram.types.rich_text_url.RichTextUrl`
     - :class:`litegram.types.rich_text_email_address.RichTextEmailAddress`
     - :class:`litegram.types.rich_text_phone_number.RichTextPhoneNumber`
     - :class:`litegram.types.rich_text_bank_card_number.RichTextBankCardNumber`
     - :class:`litegram.types.rich_text_ton_address.RichTextTonAddress`
     - :class:`litegram.types.rich_text_mention.RichTextMention`
     - :class:`litegram.types.rich_text_hashtag.RichTextHashtag`
     - :class:`litegram.types.rich_text_cashtag.RichTextCashtag`
     - :class:`litegram.types.rich_text_bot_command.RichTextBotCommand`
     - :class:`litegram.types.rich_text_button.RichTextButton`
     - :class:`litegram.types.rich_text_anchor.RichTextAnchor`
     - :class:`litegram.types.rich_text_anchor_link.RichTextAnchorLink`
     - :class:`litegram.types.rich_text_reference.RichTextReference`
     - :class:`litegram.types.rich_text_reference_link.RichTextReferenceLink`

    Source: https://core.telegram.org/bots/api#richtext
    """
