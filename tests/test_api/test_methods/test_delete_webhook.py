import pytest

from litegram.methods import DeleteWebhook
from tests.mocked_bot import MockedBot


class TestDeleteWebhook:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteWebhook, ok=True, result=True)

        response: bool = await bot.delete_webhook()
        bot.get_request()
        assert response == prepare_result.result
