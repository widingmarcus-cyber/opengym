#!/usr/bin/env python3
"""Verification script for Challenge 146: Memory Read-After-Write Delay"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: answer.txt exists and contains "2"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        sys.exit(0)

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "2":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '2'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '2' in answer.txt, got '{answer}'"}))

    # Test 2: store.json exists and is valid JSON
    store_path = os.path.join(SETUP_DIR, "store.json")
    if not os.path.exists(store_path):
        print(json.dumps({"test": "store_exists", "passed": False, "message": "setup/store.json does not exist"}))
        sys.exit(0)

    try:
        with open(store_path, "r") as f:
            store = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "store_exists", "passed": False, "message": f"Could not parse store.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "store_exists", "passed": True, "message": "store.json exists and is valid JSON"}))

    # Test 3: store.json has version = 2
    version = store.get("version")
    if version == 2:
        print(json.dumps({"test": "version_correct", "passed": True, "message": "store.json version is 2"}))
    else:
        print(json.dumps({"test": "version_correct", "passed": False, "message": f"Expected version 2, got {version}"}))

    # Test 4: store.json has data = "updated"
    data = store.get("data")
    if data == "updated":
        print(json.dumps({"test": "data_correct", "passed": True, "message": "store.json data is 'updated'"}))
    else:
        print(json.dumps({"test": "data_correct", "passed": False, "message": f"Expected data 'updated', got '{data}'"}))

    # Test 5: pending_write.flag should NOT exist (not persisted)
    flag_path = os.path.join(SETUP_DIR, "pending_write.flag")
    if not os.path.exists(flag_path):
        print(json.dumps({"test": "flag_gone", "passed": True, "message": "pending_write.flag does not exist (correctly not persisted)"}))
    else:
        print(json.dumps({"test": "flag_gone", "passed": False, "message": "pending_write.flag still exists -- it should have been cleaned up between sessions"}))


if __name__ == "__main__":
    main()
