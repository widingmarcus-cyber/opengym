#!/usr/bin/env python3
"""Verify that the agent recalled user preferences correctly from persisted memory."""

import json
import os
import sys

EXPECTED = {
    "preferred_language": "Rust",
    "timezone": "Asia/Tokyo",
    "theme": "dark mode",
    "shell": "fish",
    "editor": "Neovim",
}

ANSWERS_PATH = os.path.join(os.path.dirname(__file__), "..", "setup", "answers.json")


def main():
    # Check that answers.json exists
    if not os.path.exists(ANSWERS_PATH):
        print(json.dumps({
            "test": "answers_file_exists",
            "passed": False,
            "message": "setup/answers.json does not exist"
        }))
        sys.exit(0)

    # Parse answers.json
    try:
        with open(ANSWERS_PATH, "r") as f:
            answers = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({
            "test": "answers_file_valid",
            "passed": False,
            "message": f"Could not parse setup/answers.json: {e}"
        }))
        sys.exit(0)

    print(json.dumps({
        "test": "answers_file_valid",
        "passed": True,
        "message": "setup/answers.json exists and is valid JSON"
    }))

    # Check each expected field
    all_correct = True
    for field, expected_value in EXPECTED.items():
        actual = answers.get(field)
        if actual is None:
            passed = False
            message = f"Field '{field}' is missing from answers"
        elif actual.strip().lower() != expected_value.strip().lower():
            passed = False
            message = f"Field '{field}': expected '{expected_value}', got '{actual}'"
        else:
            passed = True
            message = f"Field '{field}' is correct: '{actual}'"

        if not passed:
            all_correct = False

        print(json.dumps({
            "test": f"recall_{field}",
            "passed": passed,
            "message": message
        }))

    # Summary
    print(json.dumps({
        "test": "all_fields_correct",
        "passed": all_correct,
        "message": "All 5 fields recalled correctly" if all_correct else "Some fields were incorrect or missing"
    }))


if __name__ == "__main__":
    main()
