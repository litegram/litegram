from __future__ import annotations

from .base import TelegramObject


class RevenueWithdrawalState(TelegramObject):
    """
    This object describes the state of a revenue withdrawal operation. Currently, it can be one of

     - :class:`litegram.types.revenue_withdrawal_state_pending.RevenueWithdrawalStatePending`
     - :class:`litegram.types.revenue_withdrawal_state_succeeded.RevenueWithdrawalStateSucceeded`
     - :class:`litegram.types.revenue_withdrawal_state_failed.RevenueWithdrawalStateFailed`

    Source: https://core.telegram.org/bots/api#revenuewithdrawalstate
    """
