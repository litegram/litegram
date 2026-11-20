from __future__ import annotations

from enum import Enum


class WidgetQueryTypeType(str, Enum):
    """
    This object represents the type of a widgetquerytype object.

    Source: https://core.telegram.org/bots/api#widgetquerytype
    """

    DATA = "data"
    SENT_TRANSACTION = "sent_transaction"
    SIGN_DATA = "sign_data"
