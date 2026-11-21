from __future__ import annotations

from unittest.mock import AsyncMock, patch

from click.testing import CliRunner
from litestar import Litestar

from litegram import Dispatcher
from litegram.cli.main import litegram_group
from litegram.exceptions import TelegramAPIError
from litegram.methods import GetMe


class TestCliErrorPaths:
    @patch("litegram.cli.main.import_string", side_effect=ImportError("bad module"))
    def test_polling_import_error(self, _mock_import):
        result = CliRunner().invoke(litegram_group, ["run", "polling", "missing:dp", "--token", "42:TEST"])
        assert result.exit_code == 1
        assert "Error: bad module" in result.output

    @patch("litegram.cli.main.import_string", return_value=object())
    def test_polling_requires_dispatcher(self, _mock_import):
        result = CliRunner().invoke(litegram_group, ["run", "polling", "app:obj", "--token", "42:TEST"])
        assert result.exit_code == 1
        assert "Dispatcher instance" in result.output

    @patch("litegram.cli.main.import_string", return_value=Dispatcher())
    def test_polling_requires_token(self, _mock_import):
        result = CliRunner().invoke(litegram_group, ["run", "polling", "app:dp"])
        assert result.exit_code == 1
        assert "token is required" in result.output

    @patch("asyncio.run", side_effect=KeyboardInterrupt)
    @patch("litegram.cli.main.import_string", return_value=Dispatcher)
    def test_polling_factory_and_keyboard_interrupt(self, _mock_import, mock_run):
        result = CliRunner().invoke(litegram_group, ["run", "polling", "app:make_dp", "--token", "42:TEST"])
        assert result.exit_code == 0
        assert "Stopped." in result.output
        mock_run.assert_called_once()

    @patch("litegram.cli.main.import_string", side_effect=ImportError("bad module"))
    def test_webhook_import_error(self, _mock_import):
        result = CliRunner().invoke(litegram_group, ["run", "webhook", "missing:app"])
        assert result.exit_code == 1
        assert "Error: bad module" in result.output

    @patch("litegram.cli.main.import_string", return_value=object())
    def test_webhook_requires_litestar(self, _mock_import):
        result = CliRunner().invoke(litegram_group, ["run", "webhook", "app:obj"])
        assert result.exit_code == 1
        assert "Litestar instance" in result.output

    @patch("uvicorn.run")
    @patch("litegram.cli.main.import_string", return_value=lambda: Litestar(route_handlers=[]))
    def test_webhook_factory(self, _mock_import, mock_run):
        result = CliRunner().invoke(litegram_group, ["run", "webhook", "app:make_app"])
        assert result.exit_code == 0
        mock_run.assert_called_once()

    def test_bot_info_requires_token(self):
        result = CliRunner().invoke(litegram_group, ["bot", "info"])
        assert result.exit_code == 1
        assert "token is required" in result.output

    @patch("litegram.Bot.get_me", new_callable=AsyncMock)
    def test_bot_info_api_error(self, mock_get_me):
        mock_get_me.side_effect = TelegramAPIError(method=GetMe(), message="api exploded")
        result = CliRunner().invoke(litegram_group, ["bot", "info", "--token", "42:TEST"])
        assert result.exit_code == 1
        assert "api exploded" in result.output
