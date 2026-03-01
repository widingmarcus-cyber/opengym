"""Tests for Challenge 016: Fix the Silent Failures."""

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from pipeline import validate, transform, aggregate, process_records


# --- validate ---

def test_validate_filters_complete_records():
    records = [
        {"name": "Alice", "amount": 100},
        {"name": "Bob"},
        {"amount": 50},
        {"name": "Carol", "amount": 200},
    ]
    result = validate(records)
    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Carol"


def test_validate_raises_on_non_list():
    with pytest.raises(TypeError):
        validate("not a list")


# --- transform ---

def test_transform_uppercases_and_converts():
    records = [{"name": "alice", "amount": "99.5"}]
    result = transform(records)
    assert result[0]["name"] == "ALICE"
    assert result[0]["amount"] == 99.5
    assert result[0]["processed"] is True


def test_transform_raises_on_bad_amount():
    records = [{"name": "bob", "amount": "not_a_number"}]
    with pytest.raises(ValueError):
        transform(records)


# --- aggregate ---

def test_aggregate_sums_correctly():
    records = [
        {"name": "ALICE", "amount": 100.0, "processed": True},
        {"name": "BOB", "amount": 50.0, "processed": True},
    ]
    result = aggregate(records)
    assert result["total_amount"] == 150.0
    assert result["count"] == 2
    assert result["names"] == ["ALICE", "BOB"]


def test_aggregate_raises_on_non_list():
    with pytest.raises(TypeError):
        aggregate(42)


# --- process_records (full pipeline) ---

def test_process_records_end_to_end():
    records = [
        {"name": "alice", "amount": "100"},
        {"name": "bob", "amount": "50"},
        {"color": "red"},
    ]
    result = process_records(records)
    assert result["total_amount"] == 150.0
    assert result["count"] == 2
    assert result["names"] == ["ALICE", "BOB"]


def test_process_records_propagates_type_error():
    with pytest.raises(TypeError):
        process_records("not a list")


def test_validate_raises_typeerror_on_string():
    """validate() must raise TypeError when given a string, not silently return []."""
    result_or_exc = None
    try:
        result_or_exc = validate("not a list")
    except TypeError:
        result_or_exc = "raised"
    assert result_or_exc == "raised", (
        f"validate('not a list') returned {result_or_exc!r} instead of raising TypeError"
    )


def test_transform_raises_valueerror_on_bad_data():
    """transform() must raise ValueError on unconvertible amount, not silently return []."""
    records = [{"name": "alice", "amount": "not_a_number"}]
    result_or_exc = None
    try:
        result_or_exc = transform(records)
    except ValueError:
        result_or_exc = "raised"
    assert result_or_exc == "raised", (
        f"transform() returned {result_or_exc!r} instead of raising ValueError"
    )


def test_no_bare_except_in_source():
    """Source code of validate, transform, aggregate must not contain bare except clauses."""
    import inspect

    for func in (validate, transform, aggregate):
        source = inspect.getsource(func)
        lines = source.split("\n")
        for line in lines:
            stripped = line.strip()
            # Bare 'except:' catches everything silently
            assert stripped != "except:", (
                f"{func.__name__} contains a bare 'except:' — errors are silently swallowed"
            )
            # 'except Exception:' is nearly as bad — too broad
            assert not stripped.startswith("except Exception:"), (
                f"{func.__name__} contains 'except Exception:' — errors are silently swallowed"
            )
