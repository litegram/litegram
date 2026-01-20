from __future__ import annotations

from sys import version_info
from typing import TYPE_CHECKING

import pytest

from litegram.dispatcher.event.handler import HandlerObject

if TYPE_CHECKING:
    from litegram.types import Message


@pytest.mark.skipif(version_info < (3, 14), reason="Requires Python >=3.14 for TypeError on unresolved ForwardRef")
def test_forward_ref_in_callback():
    def my_handler(message: Message):
        pass

    HandlerObject(callback=my_handler)


def test_forward_ref_in_callback_with_str_annotation():
    def my_handler(message: Message):
        pass

    handler = HandlerObject(callback=my_handler)
    assert "message" in handler.params
