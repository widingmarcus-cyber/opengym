"""Verification script for Challenge 115: Retry and Adapt.
Outputs JSON lines with test results.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from solution import process_data


def run_test(name, func):
    """Run a single test and return JSON result."""
    try:
        func()
        return {"test": name, "passed": True}
    except Exception as e:
        return {"test": name, "passed": False, "error": str(e)}


def test_basic_grouping():
    records = [
        {"category": "A", "value": 10},
        {"category": "A", "value": 20},
        {"category": "B", "value": 30},
    ]
    result = process_data(records)
    assert result == {"A": 15.0, "B": 30.0}, f"Expected {{'A': 15.0, 'B': 30.0}}, got {result}"


def test_empty_input():
    result = process_data([])
    assert result == {}, f"Expected {{}}, got {result}"


def test_missing_category():
    records = [
        {"value": 10},
        {"category": "A", "value": 20},
    ]
    result = process_data(records)
    assert result == {"uncategorized": 10.0, "A": 20.0}, f"Expected {{'uncategorized': 10.0, 'A': 20.0}}, got {result}"


def test_non_numeric_values():
    records = [
        {"category": "A", "value": 10},
        {"category": "A", "value": "N/A"},
    ]
    result = process_data(records)
    assert result == {"A": 10.0}, f"Expected {{'A': 10.0}}, got {result}"


def test_single_category():
    records = [
        {"category": "X", "value": 5},
        {"category": "X", "value": 15},
    ]
    result = process_data(records)
    assert result == {"X": 10.0}, f"Expected {{'X': 10.0}}, got {result}"


if __name__ == "__main__":
    tests = [
        ("test_basic_grouping", test_basic_grouping),
        ("test_empty_input", test_empty_input),
        ("test_missing_category", test_missing_category),
        ("test_non_numeric_values", test_non_numeric_values),
        ("test_single_category", test_single_category),
    ]

    all_passed = True
    for name, func in tests:
        result = run_test(name, func)
        print(json.dumps(result))
        if not result["passed"]:
            all_passed = False

    sys.exit(0 if all_passed else 1)
