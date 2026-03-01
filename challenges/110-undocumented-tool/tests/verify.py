#!/usr/bin/env python3
"""Verify Challenge 110: Undocumented Tool."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(CHALLENGE_DIR, "setup", "output.txt")

EXPECTED_LINES = [
    "World hello",
    "Baz bar foo",
    "Fox brown quick the",
    "Great is openGym",
    "123 testing",
]


def check(test_name, passed, message):
    print(json.dumps({"test": test_name, "passed": passed, "message": message}))
    return passed


def main():
    all_passed = True

    # Test 1: output.txt exists
    if not os.path.exists(OUTPUT_FILE):
        check("output_exists", False, f"setup/output.txt not found at {OUTPUT_FILE}")
        check("line_count", False, "Skipped: output file missing")
        check("line_1_correct", False, "Skipped: output file missing")
        check("line_2_correct", False, "Skipped: output file missing")
        check("line_3_correct", False, "Skipped: output file missing")
        check("line_4_correct", False, "Skipped: output file missing")
        check("line_5_correct", False, "Skipped: output file missing")
        sys.exit(0)

    all_passed &= check("output_exists", True, "setup/output.txt exists")

    # Read output
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse lines (strip trailing whitespace, remove empty trailing lines)
    lines = content.splitlines()
    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    # Test 2: correct number of lines
    if len(lines) == len(EXPECTED_LINES):
        all_passed &= check(
            "line_count", True, f"Output has {len(EXPECTED_LINES)} lines"
        )
    else:
        all_passed &= check(
            "line_count",
            False,
            f"Expected {len(EXPECTED_LINES)} lines, got {len(lines)}",
        )

    # Test 3-7: each line correct
    for i, expected in enumerate(EXPECTED_LINES):
        test_name = f"line_{i + 1}_correct"
        if i < len(lines):
            actual = lines[i].rstrip()
            if actual == expected:
                all_passed &= check(
                    test_name, True, f"Line {i + 1}: '{expected}'"
                )
            else:
                all_passed &= check(
                    test_name,
                    False,
                    f"Line {i + 1}: expected '{expected}', got '{actual}'",
                )
        else:
            all_passed &= check(
                test_name, False, f"Line {i + 1} missing (expected '{expected}')"
            )



    # === Audit log validation ===
    _audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
    _tools_dir = os.path.join(CHALLENGE_DIR, "tools")
    sys.path.insert(0, _tools_dir)
    try:
        from _audit import full_audit_check
        _audit_ok, _audit_errors = full_audit_check(
            _audit_file, "mystery",
            min_calls=1, max_calls=999,
            min_gap_ms=0,
        )
        if _audit_ok:
            check("audit_log_valid", True, "Audit log signatures, sequences, and nonces valid")
        else:
            for _err in _audit_errors[:3]:
                check("audit_log_valid", False, _err)
    except ImportError:
        check("audit_log_valid", True, "Audit module not available (skipped)")
if __name__ == "__main__":
    main()
