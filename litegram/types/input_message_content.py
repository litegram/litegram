from __future__ import annotations

from .base import MutableTelegramObject


class InputMessageContent(MutableTelegramObject):
    """
    This object represents the content of a message to be sent as a result of an inline query. Telegram clients currently support the following types:

     - :class:`litegram.types.input_text_message_content.InputTextMessageContent`
     - :class:`litegram.types.input_rich_message_content.InputRichMessageContent`
     - :class:`litegram.types.input_location_message_content.InputLocationMessageContent`
     - :class:`litegram.types.input_venue_message_content.InputVenueMessageContent`
     - :class:`litegram.types.input_contact_message_content.InputContactMessageContent`
     - :class:`litegram.types.input_invoice_message_content.InputInvoiceMessageContent`
     - :class:`litegram.types.input_widget_message_content.InputWidgetMessageContent`
     - :class:`litegram.types.input_shared_widget_message_content.InputSharedWidgetMessageContent`

    Source: https://core.telegram.org/bots/api#inputmessagecontent
    """
