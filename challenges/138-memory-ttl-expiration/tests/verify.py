#!/usr/bin/env python3
"""Verification script for Challenge 138: Memory TTL Expiration"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

VALID_KEYS = {"token_main", "token_backup"}
EXPIRED_KEYS = {"session_1", "session_2", "session_3"}


def main():
    # Test 1: active_cache.json exists
    active_path = os.path.join(SETUP_DIR, "active_cache.json")
    if not os.path.exists(active_path):
        print(json.dumps({"test": "active_cache_exists", "passed": False, "message": "setup/active_cache.json does not exist"}))
        sys.exit(0)

    print(json.dumps({"test": "active_cache_exists", "passed": True, "message": "setup/active_cache.json exists"}))

    # Test 2: active_cache.json is valid JSON
    try:
        with open(active_path, "r") as f:
            active = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "active_cache_valid_json", "passed": False, "message": f"Could not parse active_cache.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "active_cache_valid_json", "passed": True, "message": "active_cache.json is valid JSON"}))

    # Test 3: active_cache.json is a list
    if not isinstance(active, list):
        print(json.dumps({"test": "active_cache_is_list", "passed": False, "message": f"Expected a JSON array, got {type(active).__name__}"}))
        sys.exit(0)

    print(json.dumps({"test": "active_cache_is_list", "passed": True, "message": "active_cache.json is a JSON array"}))

    # Test 4: Exactly 2 entries remain
    if len(active) == 2:
        print(json.dumps({"test": "entry_count", "passed": True, "message": "active_cache.json has exactly 2 entries"}))
    else:
        print(json.dumps({"test": "entry_count", "passed": False, "message": f"Expected 2 entries, got {len(active)}"}))

    # Test 5: Only valid (non-expired) keys are present
    active_keys = set()
    for entry in active:
        if isinstance(entry, dict) and "key" in entry:
            active_keys.add(entry["key"])

    has_valid = VALID_KEYS.issubset(active_keys)
    has_expired = bool(EXPIRED_KEYS & active_keys)

    if has_valid and not has_expired:
        print(json.dumps({"test": "correct_entries", "passed": True, "message": "Only non-expired entries (token_main, token_backup) are present"}))
    elif has_expired:
        found_expired = EXPIRED_KEYS & active_keys
        print(json.dumps({"test": "correct_entries", "passed": False, "message": f"Expired entries still present: {sorted(found_expired)}"}))
    else:
        missing = VALID_KEYS - active_keys
        print(json.dumps({"test": "correct_entries", "passed": False, "message": f"Missing valid entries: {sorted(missing)}"}))

    # Test 6: Entries preserve original structure
    all_fields_ok = True
    required_fields = {"key", "value", "ttl_seconds", "created_at"}
    for entry in active:
        if not isinstance(entry, dict):
            all_fields_ok = False
            break
        if not required_fields.issubset(entry.keys()):
            all_fields_ok = False
            break

    if all_fields_ok:
        print(json.dumps({"test": "entry_structure", "passed": True, "message": "All entries have required fields (key, value, ttl_seconds, created_at)"}))
    else:
        print(json.dumps({"test": "entry_structure", "passed": False, "message": "Some entries are missing required fields (key, value, ttl_seconds, created_at)"}))


if __name__ == "__main__":
    main()
