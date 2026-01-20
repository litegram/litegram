from __future__ import annotations

from unittest.mock import MagicMock, patch

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
