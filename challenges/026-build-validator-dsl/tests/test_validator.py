"""Tests for Challenge 026: Build Validator DSL."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from validator import validate, ValidationResult


def test_valid_data():
    schema = {"name": {"type": "str", "required": True}}
    result = validate({"name": "Alice"}, schema)
    assert result.is_valid is True
    assert result.errors == []


def test_missing_required_field():
    schema = {"name": {"type": "str", "required": True}}
    result = validate({}, schema)
    assert result.is_valid is False
    assert len(result.errors) >= 1


def test_missing_optional_field():
    schema = {"nickname": {"type": "str"}}
    result = validate({}, schema)
    assert result.is_valid is True
    assert result.errors == []


def test_wrong_type():
    schema = {"age": {"type": "int"}}
    result = validate({"age": "twenty"}, schema)
    assert result.is_valid is False
    assert len(result.errors) >= 1


def test_min_max_int():
    schema = {"age": {"type": "int", "min": 0, "max": 150}}
    assert validate({"age": 25}, schema).is_valid is True
    assert validate({"age": -1}, schema).is_valid is False
    assert validate({"age": 200}, schema).is_valid is False


def test_min_max_length_str():
    schema = {"name": {"type": "str", "min_length": 2, "max_length": 10}}
    assert validate({"name": "Al"}, schema).is_valid is True
    assert validate({"name": "A"}, schema).is_valid is False
    assert validate({"name": "A" * 11}, schema).is_valid is False


def test_pattern():
    schema = {"email": {"type": "str", "pattern": "^[^@]+@[^@]+$"}}
    assert validate({"email": "user@example.com"}, schema).is_valid is True
    assert validate({"email": "invalid"}, schema).is_valid is False


def test_list_type():
    schema = {"tags": {"type": "list"}}
    assert validate({"tags": ["a", "b"]}, schema).is_valid is True
    assert validate({"tags": "not a list"}, schema).is_valid is False


def test_list_items_validation():
    schema = {"tags": {"type": "list", "items": {"type": "str"}}}
    assert validate({"tags": ["a", "b"]}, schema).is_valid is True
    result = validate({"tags": ["a", 123]}, schema)
    assert result.is_valid is False
    assert len(result.errors) >= 1


def test_multiple_fields():
    schema = {
        "name": {"type": "str", "required": True, "min_length": 1},
        "age": {"type": "int", "min": 0},
        "active": {"type": "bool"},
    }
    result = validate({"name": "Alice", "age": 30, "active": True}, schema)
    assert result.is_valid is True

    result = validate({"name": "", "age": -5, "active": "yes"}, schema)
    assert result.is_valid is False
    assert len(result.errors) >= 3


def test_float_type_with_min_max():
    schema = {"score": {"type": "float", "min": 0.0, "max": 100.0}}
    assert validate({"score": 85.5}, schema).is_valid is True
    assert validate({"score": -1.0}, schema).is_valid is False
    assert validate({"score": 101.0}, schema).is_valid is False


def test_dict_type():
    schema = {"metadata": {"type": "dict"}}
    assert validate({"metadata": {"key": "value"}}, schema).is_valid is True
    assert validate({"metadata": "not a dict"}, schema).is_valid is False
