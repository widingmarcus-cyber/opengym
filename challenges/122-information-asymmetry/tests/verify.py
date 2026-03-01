#!/usr/bin/env python3
"""Verify Challenge 122: Information Asymmetry — agents diagnosed and fixed the legacy ID bug."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
MESSAGES_PATH = os.path.join(SETUP_DIR, "messages.json")

# Add setup dir to path so we can import the modules
sys.path.insert(0, SETUP_DIR)

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def main():
    # Test 1: messages.json exists and contains diagnosis info
    if os.path.exists(MESSAGES_PATH):
        try:
            with open(MESSAGES_PATH, "r") as f:
                content = f.read()
            check(
                "messages_json_exists",
                len(content) > 20,
                "messages.json exists and has content",
            )
        except Exception as e:
            check("messages_json_exists", False, f"Could not read messages.json: {e}")
    else:
        check("messages_json_exists", False, "messages.json not found")

    # Test 2-4: Import and test the fixed service
    try:
        from services.user import UserService

        service = UserService()

        # Test 2: Legacy lookup — user_id=42 should find "L-42" record
        alice = service.get_profile(42)
        check(
            "legacy_lookup_works",
            alice is not None and alice.get("name") == "Alice",
            f"get_profile(42) should return Alice record, got: {alice}",
        )

        # Test 3: Integer lookup still works
        bob = service.get_profile(43)
        check(
            "integer_lookup_works",
            bob is not None and bob.get("name") == "Bob",
            f"get_profile(43) should return Bob record, got: {bob}",
        )

        # Test 4: Unknown ID returns None
        unknown = service.get_profile(999)
        check(
            "unknown_id_returns_none",
            unknown is None,
            f"get_profile(999) should return None, got: {unknown}",
        )

    except ImportError as e:
        check("legacy_lookup_works", False, f"Could not import UserService: {e}")
        check("integer_lookup_works", False, f"Could not import UserService: {e}")
        check("unknown_id_returns_none", False, f"Could not import UserService: {e}")
    except Exception as e:
        check("legacy_lookup_works", False, f"Unexpected error: {e}")
        check("integer_lookup_works", False, f"Unexpected error: {e}")
        check("unknown_id_returns_none", False, f"Unexpected error: {e}")

    # Test 5: Legacy ID fallback — get_profile(42) must return a dict with legacy user data
    try:
        from services.user import UserService

        service = UserService()
        alice = service.get_profile(42)
        has_email = alice is not None and alice.get("email") == "alice@legacy.com"
        check(
            "legacy_id_has_correct_email",
            has_email,
            f"get_profile(42) should return Alice with email alice@legacy.com, got: {alice}",
        )
    except Exception as e:
        check("legacy_id_has_correct_email", False, f"Error testing legacy email: {e}")

    # Test 6: messages.json contains meaningful diagnostic content (not empty or trivial)
    if os.path.exists(MESSAGES_PATH):
        try:
            with open(MESSAGES_PATH, "r") as f:
                data = json.load(f)
            # Must be a non-trivial structure with actual content
            content_str = json.dumps(data)
            has_substance = len(content_str) > 50
            check(
                "messages_json_has_substance",
                has_substance,
                f"messages.json should have meaningful diagnostic content (got {len(content_str)} chars)",
            )
        except json.JSONDecodeError:
            check("messages_json_has_substance", False, "messages.json is not valid JSON")
        except Exception as e:
            check("messages_json_has_substance", False, f"Error reading messages.json: {e}")
    else:
        check("messages_json_has_substance", False, "messages.json not found")

    # Test 7: messages.json contains fix_instructions field
    if os.path.exists(MESSAGES_PATH):
        try:
            with open(MESSAGES_PATH, "r") as f:
                data = json.load(f)
            content_str = json.dumps(data).lower()
            has_fix = "fix_instructions" in content_str or "fix" in content_str
            check(
                "messages_json_has_fix_info",
                has_fix,
                "messages.json should contain fix instructions or fix-related content",
            )
        except Exception as e:
            check("messages_json_has_fix_info", False, f"Error checking messages.json: {e}")
    else:
        check("messages_json_has_fix_info", False, "messages.json not found")

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
