import pytest

from litegram.methods import SetWebhook
from tests.mocked_bot import MockedBot


class TestSetWebhook:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetWebhook, ok=True, result=True)

        response: bool = await bot.set_webhook(url="https://example.com")
        bot.get_request()
        assert response == prepare_result.result
