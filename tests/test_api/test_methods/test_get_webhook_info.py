from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetWebhookInfo
from litegram.types import WebhookInfo

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetWebhookInfo:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetWebhookInfo,
            ok=True,
            result=WebhookInfo(url="https://example.com", has_custom_certificate=False, pending_update_count=0),
        )

        response: WebhookInfo = await bot.get_webhook_info()
        bot.get_request()
        assert response == prepare_result.result
