"""Tests for Challenge 007: Find in the Docs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    api_version,
    rate_limit,
    max_widget_name_length,
    token_expiry_seconds,
    delete_restore_days,
    bulk_max_size,
    webhook_max_retries,
    python_sdk_version,
    error_code_for_expired_token,
    widget_categories,
)


def test_api_version():
    assert api_version() == "3.2.1"


def test_rate_limit():
    assert rate_limit() == 500


def test_max_widget_name_length():
    assert max_widget_name_length() == 128


def test_token_expiry():
    assert token_expiry_seconds() == 3600


def test_delete_restore_days():
    assert delete_restore_days() == 90


def test_bulk_max_size():
    assert bulk_max_size() == 1000


def test_webhook_max_retries():
    assert webhook_max_retries() == 5


def test_python_sdk_version():
    assert python_sdk_version() == "2.1.0"


def test_error_code_for_expired_token():
    assert error_code_for_expired_token() == "TOKEN_EXPIRED"


def test_widget_categories():
    result = widget_categories()
    assert result == ["enterprise", "premium", "standard"]
