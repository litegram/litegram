from __future__ import annotations

import pytest

from litegram.exceptions import DetailedLitegramError


class TestException:
    @pytest.mark.parametrize(
        "message,result",
        [
            ["reason", "DetailedLitegramError('reason')"],
        ],
    )
    def test_representation(self, message: str, result: str):
        exc = DetailedLitegramError(message=message)
        assert repr(exc) == result
