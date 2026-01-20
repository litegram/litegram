from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner
from litestar import Litestar

from litegram import Dispatcher
from litegram.cli.main import import_string, litegram_group


def test_import_string_module():
    import os

    assert import_string("os") is os


def test_import_string_obj():
    from os import path

    assert import_string("os:path") is path


def test_import_string_error():
    with pytest.raises(ImportError):
        import_string("non_existent_module")
    with pytest.raises(ImportError):
        import_string("os:non_existent_attr")


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(litegram_group, ["version"])
    assert result.exit_code == 0
    assert "litegram" in result.output


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(litegram_group, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "run" in result.output


def test_cli_run_help():
    runner = CliRunner()
    result = runner.invoke(litegram_group, ["run", "--help"])
    assert result.exit_code == 0
    assert "polling" in result.output
    assert "webhook" in result.output


@patch("litegram.cli.main.import_string")
@patch("asyncio.run")
def test_cli_run_polling(mock_run, mock_import):
    dp = Dispatcher()
    mock_import.return_value = dp

    runner = CliRunner()
    result = runner.invoke(litegram_group, ["run", "polling", "app:dp", "--token", "123:ABC"])

    assert result.exit_code == 0
    assert "Starting polling" in result.output
    mock_run.assert_called_once()


@patch("litegram.cli.main.import_string")
@patch("uvicorn.run")
def test_cli_run_webhook(mock_uvicorn_run, mock_import):
    app = Litestar(route_handlers=[])
    mock_import.return_value = app

    runner = CliRunner()
    result = runner.invoke(litegram_group, ["run", "webhook", "app:app"])

    assert result.exit_code == 0
    mock_uvicorn_run.assert_called_once()


def test_cli_bot_help():
    runner = CliRunner()
    result = runner.invoke(litegram_group, ["bot", "--help"])
    assert result.exit_code == 0
    assert "info" in result.output


@patch("litegram.Bot.get_me", new_callable=AsyncMock)
def test_cli_bot_info(mock_get_me):
    from litegram.types import User

    mock_get_me.return_value = User(
        id=42,
        is_bot=True,
        first_name="Test",
        username="test_bot",
        can_join_groups=True,
        can_read_all_group_messages=True,
        supports_inline_queries=False,
    )

    runner = CliRunner()
    result = runner.invoke(litegram_group, ["bot", "info", "--token", "123:ABC"])

    assert result.exit_code == 0
    assert "Bot information:" in result.output
    assert "test_bot" in result.output


def test_cli_i18n_help():
    runner = CliRunner()
    result = runner.invoke(litegram_group, ["i18n", "--help"])
    assert result.exit_code == 0
    assert "extract" in result.output
    assert "init" in result.output
    assert "update" in result.output
    assert "compile" in result.output


@patch("babel.messages.frontend.CommandLineInterface.run")
def test_cli_i18n_commands(mock_babel_run):
    runner = CliRunner()

    # Test extract
    result = runner.invoke(litegram_group, ["i18n", "extract"])
    assert result.exit_code == 0
    assert mock_babel_run.called

    # Test init
    mock_babel_run.reset_mock()
    result = runner.invoke(litegram_group, ["i18n", "init", "en"])
    assert result.exit_code == 0
    assert mock_babel_run.called

    # Test update
    mock_babel_run.reset_mock()
    result = runner.invoke(litegram_group, ["i18n", "update"])
    assert result.exit_code == 0
    assert mock_babel_run.called

    # Test compile
    mock_babel_run.reset_mock()
    result = runner.invoke(litegram_group, ["i18n", "compile"])
    assert result.exit_code == 0
    assert mock_babel_run.called
