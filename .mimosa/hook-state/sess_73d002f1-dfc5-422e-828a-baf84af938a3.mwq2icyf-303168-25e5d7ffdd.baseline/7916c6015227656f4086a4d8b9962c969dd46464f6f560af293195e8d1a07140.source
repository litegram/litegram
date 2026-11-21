from __future__ import annotations

from itertools import product
from typing import Any
from urllib.parse import parse_qs

import pytest

from litegram.utils.link import (
    BRANCH,
    create_channel_bot_link,
    create_telegram_link,
    create_tg_link,
    docs_url,
)


class TestLink:
    @pytest.mark.parametrize(
        "base,params,result",
        [["user", {"id": 42}, "tg://user?id=42"]],
    )
    def test_create_tg_link(self, base: str, params: dict[str, Any], result: str):
        assert create_tg_link(base, **params) == result

    @pytest.mark.parametrize(
        "base,params,result",
        [
            ["username", {}, "https://t.me/username"],
            ["username", {"start": "test"}, "https://t.me/username?start=test"],
        ],
    )
    def test_create_telegram_link(self, base: str, params: dict[str, Any], result: str):
        assert create_telegram_link(base, **params) == result

    def test_fragment(self):
        assert docs_url("test.html", fragment_="test") == f"https://litegram.readthedocs.io/en/{BRANCH}/test.html#test"

    def test_docs(self):
        assert docs_url("test.html") == f"https://litegram.readthedocs.io/en/{BRANCH}/test.html"


class TestCreateChannelBotLink:
    def test_without_params(self):
        assert create_channel_bot_link("test_bot") == "https://t.me/test_bot?startchannel"

    def test_parameter(self):
        assert (
            create_channel_bot_link("test_bot", parameter="parameter in group")
            == "https://t.me/test_bot?startgroup=parameter+in+group"
        )

    def test_startchannel_with_permissions(self):
        link = create_channel_bot_link("test_bot", post_messages=True, edit_messages=True)
        assert link == "https://t.me/test_bot?startchannel&admin=post_messages+edit_messages"

    def test_permissions(self):
        # Is bad idea to put over 2k cases into parameterized test,
        # so I've preferred to implement it inside the test

        params = {
            "change_info",
            "post_messages",
            "edit_messages",
            "delete_messages",
            "restrict_members",
            "invite_users",
            "pin_messages",
            "promote_members",
            "manage_video_chats",
            "anonymous",
            "manage_chat",
        }

        variants = product([True, False], repeat=len(params))
        for _index, variant in enumerate(variants):
            kwargs = {k: v for k, v in zip(params, variant, strict=False) if v}
            if not kwargs:
                # Variant without additional arguments is already covered
                continue

            link = create_channel_bot_link("test", **kwargs)
            query = parse_qs(link.split("?", maxsplit=1)[-1], max_num_fields=2, keep_blank_values=True)
            assert "startchannel" in query
            assert "admin" in link
            # A literal "+" in the query decodes to a space via parse_qs,
            # so compare against the raw query part.
            admin = link.split("admin=", maxsplit=1)[-1]
            assert set(admin.split("+")) == set(kwargs)
