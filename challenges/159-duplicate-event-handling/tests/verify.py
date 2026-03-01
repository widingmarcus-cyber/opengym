#!/usr/bin/env python3
"""Verification script for Challenge 159: Duplicate Event Handling"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: processed.json exists and is valid JSON
    processed_path = os.path.join(SETUP_DIR, "processed.json")
    if not os.path.exists(processed_path):
        print(json.dumps({"test": "processed_exists", "passed": False, "message": "setup/processed.json does not exist"}))
        sys.exit(0)

    try:
        with open(processed_path, "r") as f:
            processed = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "processed_valid", "passed": False, "message": f"Could not parse processed.json: {e}"}))
        sys.exit(0)

    if not isinstance(processed, list):
        print(json.dumps({"test": "processed_is_array", "passed": False, "message": "processed.json must be a JSON array"}))
        sys.exit(0)

    print(json.dumps({"test": "processed_exists", "passed": True, "message": "processed.json exists and is valid JSON array"}))

    # Test 2: processed.json has exactly 5 unique events
    if len(processed) == 5:
        print(json.dumps({"test": "processed_count", "passed": True, "message": "processed.json has 5 events"}))
    else:
        print(json.dumps({"test": "processed_count", "passed": False, "message": f"Expected 5 events, got {len(processed)}"}))

    # Test 3: No duplicate event_ids in processed.json
    event_ids = [e.get("event_id") for e in processed]
    unique_ids = set(event_ids)
    if len(event_ids) == len(unique_ids):
        print(json.dumps({"test": "no_duplicates", "passed": True, "message": "No duplicate event_ids in processed.json"}))
    else:
        duplicates = [eid for eid in event_ids if event_ids.count(eid) > 1]
        print(json.dumps({"test": "no_duplicates", "passed": False, "message": f"Found duplicate event_ids: {duplicates}"}))

    # Test 4: All expected event_ids are present
    expected_ids = {"e1", "e2", "e3", "e4", "e5"}
    if unique_ids == expected_ids:
        print(json.dumps({"test": "all_ids_present", "passed": True, "message": "All expected event_ids (e1-e5) are present"}))
    else:
        missing = expected_ids - unique_ids
        extra = unique_ids - expected_ids
        print(json.dumps({"test": "all_ids_present", "passed": False, "message": f"Missing: {missing}, Extra: {extra}"}))

    # Test 5: answer.txt exists and equals "5"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        return

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "5":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '5'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '5' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
