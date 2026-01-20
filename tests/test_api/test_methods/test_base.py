from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import sentinel

import pytest

from litegram.methods import GetMe, TelegramMethod
from litegram.types import TelegramObject, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestTelegramMethodRemoveUnset:
    @pytest.mark.parametrize(
        "values,names",
        [
            [{}, set()],
            [{"foo": "bar"}, {"foo"}],
            [{"foo": "bar", "baz": sentinel.DEFAULT}, {"foo"}],
        ],
    )
    @pytest.mark.parametrize("obj", [TelegramMethod, TelegramObject])
    def test_remove_unset(self, values, names, obj):
        validated = obj.remove_unset(values)
        assert set(validated.keys()) == names

    @pytest.mark.parametrize("obj", [TelegramMethod, TelegramObject])
    def test_remove_unset_non_dict(self, obj):
        assert obj.remove_unset("") == ""


class TestTelegramMethodCall:
    @pytest.mark.anyio
    async def test_async_emit_unsuccessful(self, bot: MockedBot):
        with pytest.raises(
            RuntimeError,
            match="This method is not mounted to a any bot instance.+",
        ):
            await GetMe()

    @pytest.mark.anyio
    async def test_async_emit(self, bot: MockedBot):
        bot.add_result_for(GetMe, ok=True, result=User(id=42, is_bot=True, first_name="Test"))
        method = GetMe().as_(bot)
        assert isinstance(await method, User)
