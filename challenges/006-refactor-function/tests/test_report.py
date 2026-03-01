"""Tests for Challenge 006: Refactor the Monster Function."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from report import generate_report, validate_records, calculate_pay, format_currency


# --- Test that refactored functions exist and work ---

def test_validate_records_exists():
    """validate_records must exist as a separate function."""
    valid = validate_records([
        {"name": "Alice", "hours": 40, "rate": 25},
        {"name": "", "hours": 40, "rate": 25},  # invalid: empty name
        {"hours": 40, "rate": 25},               # invalid: no name
        {"name": "Bob", "hours": -5, "rate": 25}, # invalid: negative hours
    ])
    assert len(valid) == 1
    assert valid[0]["name"] == "Alice"


def test_calculate_pay_regular():
    """calculate_pay must exist as a separate function."""
    assert calculate_pay(40, 25) == 1000.0
    assert calculate_pay(20, 30) == 600.0


def test_calculate_pay_overtime():
    assert calculate_pay(50, 20) == 40 * 20 + 10 * 20 * 1.5
    assert calculate_pay(45, 100) == 40 * 100 + 5 * 100 * 1.5


def test_format_currency():
    """format_currency must exist as a separate function."""
    assert format_currency(1000) == "$1,000.00"
    assert format_currency(1234567.89) == "$1,234,567.89"
    assert format_currency(0) == "$0.00"
    assert format_currency(99.9) == "$99.90"


# --- Test generate_report still works end-to-end ---

def test_generate_report_basic():
    data = [
        {"name": "Alice", "hours": 40, "rate": 25.0},
        {"name": "Bob", "hours": 50, "rate": 20.0},
    ]
    report = generate_report(data)
    assert len(report["employees"]) == 2

    alice = report["employees"][0]
    assert alice["name"] == "Alice"
    assert alice["pay"] == 1000.0
    assert alice["formatted_pay"] == "$1,000.00"

    bob = report["employees"][1]
    assert bob["pay"] == 40 * 20 + 10 * 20 * 1.5  # 1100.0


def test_generate_report_skips_invalid():
    data = [
        {"name": "Alice", "hours": 40, "rate": 25},
        "not a dict",
        {"name": "Bob", "hours": -1, "rate": 25},
        {"name": "Charlie", "hours": 10, "rate": 0},
    ]
    report = generate_report(data)
    assert len(report["employees"]) == 1


def test_generate_report_total():
    data = [
        {"name": "Alice", "hours": 40, "rate": 25.0},
        {"name": "Bob", "hours": 40, "rate": 25.0},
    ]
    report = generate_report(data)
    assert report["total"] == "$2,000.00"


def test_generate_report_empty():
    report = generate_report([])
    assert report["employees"] == []
    assert report["total"] == "$0.00"
