"""Tests for Challenge 059: Read the Schema."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from answers import (
    required_fields,
    valid_status_values,
    max_items_in_tags,
    address_pattern,
    is_field_required,
    get_field_type,
)


def test_required_fields():
    result = required_fields()
    expected = ["customer_name", "email", "items", "order_id", "shipping_address", "status"]
    assert result == expected


def test_valid_status_values():
    result = valid_status_values()
    expected = ["cancelled", "confirmed", "delivered", "pending", "processing", "shipped"]
    assert result == expected


def test_max_items_in_tags():
    assert max_items_in_tags() == 10


def test_address_pattern():
    assert address_pattern() == "^[0-9]{5}(-[0-9]{4})?$"


def test_is_field_required_true():
    assert is_field_required("shipping_address.street") is True


def test_is_field_required_false():
    assert is_field_required("shipping_address.state") is False


def test_get_field_type_direct():
    assert get_field_type("order_id") == "string"


def test_get_field_type_ref():
    assert get_field_type("priority") == "string"
