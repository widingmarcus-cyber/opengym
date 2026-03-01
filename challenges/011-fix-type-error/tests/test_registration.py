"""Tests for Challenge 011: Fix the Type Errors."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from registration import (
    create_username,
    build_profile,
    format_address,
    calculate_age_in_months,
    merge_preferences,
)


def test_create_username_basic():
    assert create_username("John", "Doe", 1990) == "john_doe_1990"


def test_create_username_mixed_case():
    assert create_username("ALICE", "Smith", 2001) == "alice_smith_2001"


def test_build_profile_returns_dict():
    result = build_profile("Alice", 30, ["python", "hiking"])
    assert isinstance(result, dict)
    assert result["name"] == "Alice"
    assert result["age"] == 30


def test_build_profile_sorts_tags():
    result = build_profile("Bob", 25, ["zebra", "apple", "mango"])
    assert result["tags"] == ["apple", "mango", "zebra"]


def test_format_address():
    assert format_address("123 Main St", "Springfield", 62704) == "123 Main St, Springfield 62704"


def test_calculate_age_in_months():
    assert calculate_age_in_months("25") == 300
    assert isinstance(calculate_age_in_months("25"), int)


def test_merge_preferences_basic():
    defaults = {"theme": "light", "lang": "en"}
    overrides = {"theme": "dark"}
    result = merge_preferences(defaults, overrides)
    assert isinstance(result, dict)
    assert result == {"theme": "dark", "lang": "en"}


def test_merge_preferences_no_overrides():
    defaults = {"volume": 50, "muted": False}
    overrides = {}
    result = merge_preferences(defaults, overrides)
    assert result == {"volume": 50, "muted": False}
