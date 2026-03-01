#!/usr/bin/env python3
"""Verification script for Challenge 147: Memory Size Cap Enforcement"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

IMPORTANT_KEYS = {
    "item_03", "item_07", "item_12", "item_18", "item_23",
    "item_29", "item_34", "item_38", "item_42", "item_47",
}


def main():
    # Test 1: memory.json exists and is valid JSON
    memory_path = os.path.join(SETUP_DIR, "memory.json")
    if not os.path.exists(memory_path):
        print(json.dumps({"test": "memory_exists", "passed": False, "message": "setup/memory.json does not exist"}))
        sys.exit(0)

    try:
        with open(memory_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "memory_exists", "passed": False, "message": f"Could not parse memory.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "memory_exists", "passed": True, "message": "memory.json exists and is valid JSON"}))

    # Test 2: memory.json is an array of records
    if not isinstance(data, list):
        print(json.dumps({"test": "memory_is_array", "passed": False, "message": f"Expected memory.json to be an array, got {type(data).__name__}"}))
        sys.exit(0)

    print(json.dumps({"test": "memory_is_array", "passed": True, "message": "memory.json is an array"}))

    # Test 3: File size does not exceed 1024 bytes
    file_size = os.path.getsize(memory_path)
    if file_size <= 1024:
        print(json.dumps({"test": "size_cap", "passed": True, "message": f"memory.json is {file_size} bytes (within 1024 byte limit)"}))
    else:
        print(json.dumps({"test": "size_cap", "passed": False, "message": f"memory.json is {file_size} bytes (exceeds 1024 byte limit)"}))

    # Test 4: All 10 IMPORTANT records are present
    stored_keys = set()
    for record in data:
        if isinstance(record, dict) and "key" in record:
            stored_keys.add(record["key"])

    missing_important = IMPORTANT_KEYS - stored_keys
    if len(missing_important) == 0:
        print(json.dumps({"test": "all_important_present", "passed": True, "message": "All 10 IMPORTANT records are present"}))
    else:
        print(json.dumps({"test": "all_important_present", "passed": False, "message": f"Missing IMPORTANT records: {sorted(missing_important)}"}))

    # Test 5: Each record has key and value fields
    all_valid = all(
        isinstance(r, dict) and "key" in r and "value" in r
        for r in data
    )
    if all_valid:
        print(json.dumps({"test": "record_structure", "passed": True, "message": "All records have 'key' and 'value' fields"}))
    else:
        print(json.dumps({"test": "record_structure", "passed": False, "message": "Some records are missing 'key' or 'value' fields"}))

    # Test 6: answer.txt exists and contains the correct count
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        sys.exit(0)

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    record_count = len(data)
    if answer == str(record_count):
        print(json.dumps({"test": "answer_correct", "passed": True, "message": f"answer.txt contains '{record_count}' matching stored record count"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"answer.txt contains '{answer}' but memory.json has {record_count} records"}))


if __name__ == "__main__":
    main()
