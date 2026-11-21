from __future__ import annotations

import runpy
from unittest.mock import patch


def test_main_module_invokes_cli_group():
    with patch("litegram.cli.litegram_group") as group:
        runpy.run_module("litegram.__main__", run_name="__main__")
        group.assert_called_once_with()
