from __future__ import annotations

import datetime

import pytest

from litegram.utils.web_app_signature import safe_check_webapp_init_data_from_signature

VALID_INIT_DATA = (
    "auth_date=1650385342&user=%7B%22id%22%3A42%2C%22first_name%22%3A%22Test%22%7D"
    "&query_id=test&hash=123"
    "&signature=JQ0JR2tjC65yq_jNZV0wuJVX6J-SWPMV0mprUXG34g-NvxL4RcF1Rz5n4VVo00VRghEUBf5t___uoeb1-jU_Cw"
)
# Test-only Ed25519 public key matching the signatures used in the fixture data.
PUBLIC_KEY = bytes.fromhex("4112765021341e5415e772cd65903f6b94e3ea1c2ab669e6d3e18ee2db00da61")


class TestMiniAppFreshness:
    def test_no_timeout_accepts_old_data(self):
        result = safe_check_webapp_init_data_from_signature(42, VALID_INIT_DATA, PUBLIC_KEY)
        assert result.auth_date.year == 2022

    def test_timeout_boundary_respected(self):
        # The fixture's auth_date is fixed in 2022; compute its exact age and
        # verify the timeout boundary is honored to the second.
        from litegram.utils.web_app import parse_webapp_init_data

        parsed = parse_webapp_init_data(VALID_INIT_DATA)
        age = datetime.datetime.now(datetime.UTC) - parsed.auth_date.replace(tzinfo=datetime.UTC)
        with pytest.raises(ValueError, match="too old"):
            safe_check_webapp_init_data_from_signature(
                42, VALID_INIT_DATA, PUBLIC_KEY, auth_date_timeout=max(age.total_seconds() - 1, 1)
            )

    def test_stale_data_rejected_with_timeout(self):
        with pytest.raises(ValueError, match="too old"):
            safe_check_webapp_init_data_from_signature(
                42, VALID_INIT_DATA, PUBLIC_KEY, auth_date_timeout=60
            )
