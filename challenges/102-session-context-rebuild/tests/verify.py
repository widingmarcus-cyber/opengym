#!/usr/bin/env python3
"""Verify that all 3 bugs in buggy_app.py have been fixed correctly."""

import json
import os
import sys

# Add the setup directory to the path so we can import buggy_app
setup_dir = os.path.join(os.path.dirname(__file__), "..", "setup")
sys.path.insert(0, setup_dir)


def test_find_pairs():
    """Test that find_pairs works without IndexError and returns correct pairs."""
    try:
        from buggy_app import find_pairs

        result = find_pairs([1, 2, 3, 4])
        expected = [(1, 2), (2, 3), (3, 4)]

        if result == expected:
            return True, f"find_pairs([1,2,3,4]) correctly returned {result}"
        else:
            return False, f"find_pairs([1,2,3,4]) returned {result}, expected {expected}"

    except IndexError as e:
        return False, f"find_pairs raised IndexError (off-by-one bug not fixed): {e}"
    except Exception as e:
        return False, f"find_pairs raised unexpected error: {type(e).__name__}: {e}"


def test_calculate_bill():
    """Test that calculate_bill uses the correct variable and returns correct values."""
    try:
        from buggy_app import calculate_bill

        result = calculate_bill([10.0, 20.0], 0.1)

        if not isinstance(result, dict):
            return False, f"calculate_bill returned {type(result).__name__}, expected dict"

        expected_subtotal = 30.0
        expected_tax = 3.0
        expected_total = 33.0

        errors = []
        if abs(result.get("subtotal", 0) - expected_subtotal) > 0.001:
            errors.append(f"subtotal: got {result.get('subtotal')}, expected {expected_subtotal}")
        if abs(result.get("tax", 0) - expected_tax) > 0.001:
            errors.append(f"tax: got {result.get('tax')}, expected {expected_tax}")
        if abs(result.get("total", 0) - expected_total) > 0.001:
            errors.append(f"total: got {result.get('total')}, expected {expected_total}")

        if errors:
            return False, f"calculate_bill([10.0, 20.0], 0.1) has errors: {'; '.join(errors)}"

        return True, f"calculate_bill correctly returned {result}"

    except NameError as e:
        return False, f"calculate_bill raised NameError (wrong variable bug not fixed): {e}"
    except Exception as e:
        return False, f"calculate_bill raised unexpected error: {type(e).__name__}: {e}"


def test_format_receipt():
    """Test that format_receipt returns a string, not None."""
    try:
        from buggy_app import format_receipt

        bill = {"subtotal": 30.0, "tax": 3.0, "total": 33.0}
        result = format_receipt(bill)

        if result is None:
            return False, "format_receipt returned None (missing return statement not fixed)"

        if not isinstance(result, str):
            return False, f"format_receipt returned {type(result).__name__}, expected str"

        if len(result.strip()) == 0:
            return False, "format_receipt returned an empty string"

        # Check that the receipt contains the expected values
        if "30.00" not in result:
            return False, f"Receipt does not contain subtotal '30.00': {result}"
        if "3.00" not in result:
            return False, f"Receipt does not contain tax '3.00': {result}"
        if "33.00" not in result:
            return False, f"Receipt does not contain total '33.00': {result}"

        return True, f"format_receipt returned a valid receipt string"

    except Exception as e:
        return False, f"format_receipt raised unexpected error: {type(e).__name__}: {e}"


def main():
    tests = [
        ("find_pairs_no_index_error", test_find_pairs),
        ("calculate_bill_correct_variable", test_calculate_bill),
        ("format_receipt_returns_string", test_format_receipt),
    ]

    all_passed = True
    for test_name, test_fn in tests:
        passed, message = test_fn()
        if not passed:
            all_passed = False
        print(json.dumps({
            "test": test_name,
            "passed": passed,
            "message": message
        }))

    print(json.dumps({
        "test": "all_bugs_fixed",
        "passed": all_passed,
        "message": "All 3 bugs fixed correctly" if all_passed else "Some bugs remain unfixed"
    }))


if __name__ == "__main__":
    main()
