#!/usr/bin/env python3
"""Verify Challenge 106: Find the Right Tool."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(CHALLENGE_DIR, "setup", "output.json")

EXPECTED_RECORDS = [
    {"name": "Alice", "age": 30, "city": "Stockholm"},
    {"name": "Bob", "age": 25, "city": "Gothenburg"},
    {"name": "Carol", "age": 35, "city": "Malmö"},
]


def check(test_name, passed, message):
    print(json.dumps({"test": test_name, "passed": passed, "message": message}))
    return passed


def main():
    all_passed = True

    # Test 1: output.json exists
    if not os.path.exists(OUTPUT_FILE):
        check("output_exists", False, f"setup/output.json not found at {OUTPUT_FILE}")
        # Can't continue without the file
        check("valid_json", False, "Skipped: output file missing")
        check("record_count", False, "Skipped: output file missing")
        check("data_correct", False, "Skipped: output file missing")
        sys.exit(0)

    all_passed &= check("output_exists", True, "setup/output.json exists")

    # Test 2: valid JSON (try utf-8 first, fall back to other encodings)
    data = None
    for encoding in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            with open(OUTPUT_FILE, "r", encoding=encoding) as f:
                data = json.load(f)
            break
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

    if data is not None:
        all_passed &= check("valid_json", True, "output.json contains valid JSON")
    else:
        check("valid_json", False, "output.json is not valid JSON or has unsupported encoding")
        check("record_count", False, "Skipped: invalid JSON")
        check("data_correct", False, "Skipped: invalid JSON")
        sys.exit(0)

    # Test 3: correct number of records
    if not isinstance(data, list):
        check("record_count", False, f"Expected a JSON array, got {type(data).__name__}")
        check("data_correct", False, "Skipped: not an array")
        sys.exit(0)

    if len(data) == 3:
        all_passed &= check("record_count", True, "Contains exactly 3 records")
    else:
        all_passed &= check(
            "record_count", False, f"Expected 3 records, got {len(data)}"
        )

    # Test 4: data correctness
    errors = []
    for expected in EXPECTED_RECORDS:
        found = False
        for record in data:
            name_match = str(record.get("name", "")) == expected["name"]
            age_match = False
            try:
                age_match = int(record.get("age", -1)) == expected["age"]
            except (ValueError, TypeError):
                pass
            city_match = str(record.get("city", "")) == expected["city"]

            if name_match and age_match and city_match:
                found = True
                break

        if not found:
            errors.append(f"Missing or incorrect record for {expected['name']}")

    if not errors:
        all_passed &= check("data_correct", True, "All records have correct data")
    else:
        all_passed &= check(
            "data_correct", False, "; ".join(errors)
        )


if __name__ == "__main__":
    main()
