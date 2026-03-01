#!/usr/bin/env python3
"""Verification script for Challenge 150: Lock Timeout"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: result.txt exists
result_path = os.path.join(SETUP_DIR, "result.txt")
if not os.path.exists(result_path):
    print(json.dumps({"test": "result_file_exists", "passed": False, "message": "result.txt does not exist"}))
    sys.exit(0)

with open(result_path, "r") as f:
    result = f.read().strip()
print(json.dumps({"test": "result_file_exists", "passed": True, "message": "result.txt exists"}))

# Test 2: result.txt contains "RECOVERED"
if result == "RECOVERED":
    print(json.dumps({"test": "result_recovered", "passed": True, "message": "result.txt contains 'RECOVERED'"}))
else:
    print(json.dumps({"test": "result_recovered", "passed": False, "message": f"Expected 'RECOVERED', got '{result}'"}))

# Test 3: lock.json exists and has locked=false
lock_path = os.path.join(SETUP_DIR, "lock.json")
if not os.path.exists(lock_path):
    print(json.dumps({"test": "lock_released", "passed": False, "message": "lock.json does not exist"}))
else:
    try:
        with open(lock_path, "r") as f:
            lock = json.load(f)
        if isinstance(lock, dict) and lock.get("locked") is False:
            print(json.dumps({"test": "lock_released", "passed": True, "message": "lock.json has locked=false (stale lock was recovered and released)"}))
        else:
            print(json.dumps({"test": "lock_released", "passed": False, "message": f"Lock not released. lock.json: {lock}"}))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "lock_released", "passed": False, "message": f"lock.json is not valid JSON: {e}"}))

# Test 4: lock.json no longer held by stale_process
if os.path.exists(lock_path):
    try:
        with open(lock_path, "r") as f:
            lock = json.load(f)
        if isinstance(lock, dict) and lock.get("holder") != "stale_process":
            print(json.dumps({"test": "stale_process_cleared", "passed": True, "message": "Stale process is no longer the lock holder"}))
        else:
            print(json.dumps({"test": "stale_process_cleared", "passed": False, "message": "Lock is still held by stale_process"}))
    except (json.JSONDecodeError, IOError):
        print(json.dumps({"test": "stale_process_cleared", "passed": False, "message": "Could not read lock.json"}))

# Test 5: answer.txt exists and equals "LOCK_RECOVERED"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "LOCK_RECOVERED":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt correctly contains 'LOCK_RECOVERED'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'LOCK_RECOVERED', got '{answer}'"}))
