from __future__ import annotations

from .base import TelegramObject


class TransactionPartner(TelegramObject):
    """
    This object describes the source of a transaction, or its recipient for outgoing transactions. Currently, it can be one of

     - :class:`litegram.types.transaction_partner_user.TransactionPartnerUser`
     - :class:`litegram.types.transaction_partner_chat.TransactionPartnerChat`
     - :class:`litegram.types.transaction_partner_affiliate_program.TransactionPartnerAffiliateProgram`
     - :class:`litegram.types.transaction_partner_fragment.TransactionPartnerFragment`
     - :class:`litegram.types.transaction_partner_telegram_ads.TransactionPartnerTelegramAds`
     - :class:`litegram.types.transaction_partner_telegram_api.TransactionPartnerTelegramApi`
     - :class:`litegram.types.transaction_partner_other.TransactionPartnerOther`

    Source: https://core.telegram.org/bots/api#transactionpartner
    """
