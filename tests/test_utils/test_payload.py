from __future__ import annotations

from typing import Any

import pytest

from litegram.utils.payload import decode_payload, encode_payload


class TestPayload:
    @pytest.mark.parametrize(
        "payload,expected",
        [
            ("foo", "Zm9v"),
            ("fo", "Zm8"),
            ("f", "Zg"),
            ("", ""),
            ("12345", "MTIzNDU"),
            ("hello world", "aGVsbG8gd29ybGQ"),
            ("underscore_and-dash", "dW5kZXJzY29yZV9hbmQtZGFzaA"),
        ],
    )
    def test_encode_payload(self, payload: str, expected: str):
        assert encode_payload(payload) == expected

    @pytest.mark.parametrize(
        "payload",
        [
            "foo",
            "fo",
            "f",
            "",
            "12345",
            "hello world",
            "underscore_and-dash",
            "symbols!@#$%^&*()_+",
        ],
    )
    def test_decode_payload(self, payload: str):
        encoded = encode_payload(payload)
        assert decode_payload(encoded) == payload

    @pytest.mark.parametrize(
        "payload,expected_decoded",
        [
            (123, "123"),
            (True, "True"),
            (None, "None"),
        ],
    )
    def test_encode_non_string_payload(self, payload: Any, expected_decoded: str):
        encoded = encode_payload(payload)
        assert decode_payload(encoded) == expected_decoded

    def test_custom_encoder_decoder(self):
        def xor_encoder(data: bytes) -> bytes:
            return bytes(b ^ 0x42 for b in data)

        def xor_decoder(data: bytes) -> bytes:
            return bytes(b ^ 0x42 for b in data)

        payload = "secret message"
        encoded = encode_payload(payload, encoder=xor_encoder)

        # Verify it's encoded differently than standard
        standard_encoded = encode_payload(payload)
        assert encoded != standard_encoded

        # Verify decoding works with custom decoder
        decoded = decode_payload(encoded, decoder=xor_decoder)
        assert decoded == payload

    def test_decode_invalid_base64(self):
        # Current implementation of _decode_b64 and urlsafe_b64decode
        # seems to be very lenient and returns empty bytes for "!!!"
        # instead of raising an error.
        result = decode_payload("!!!")
        assert result == ""
