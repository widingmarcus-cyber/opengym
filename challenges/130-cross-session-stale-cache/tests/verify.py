#!/usr/bin/env python3
"""Verification script for Challenge 130: Cross-Session Stale Cache"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: state.json exists and is valid JSON
state_path = os.path.join(SETUP_DIR, "state.json")
if not os.path.exists(state_path):
    print(json.dumps({"test": "state_file_exists", "passed": False, "message": "state.json does not exist"}))
    sys.exit(0)

try:
    with open(state_path, "r") as f:
        state = json.load(f)
    print(json.dumps({"test": "state_file_exists", "passed": True, "message": "state.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "state_file_exists", "passed": False, "message": f"state.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: state.json has counter = 2
if isinstance(state, dict):
    counter = state.get("counter")
    if counter == 2:
        print(json.dumps({"test": "counter_is_2", "passed": True, "message": "state.json has counter = 2"}))
    else:
        print(json.dumps({"test": "counter_is_2", "passed": False, "message": f"Expected counter = 2, got counter = {counter}"}))
else:
    print(json.dumps({"test": "counter_is_2", "passed": False, "message": "state.json is not a JSON object (dict)"}))

# Test 3: state.json has status = "updated"
if isinstance(state, dict):
    status = state.get("status")
    if status == "updated":
        print(json.dumps({"test": "status_is_updated", "passed": True, "message": "state.json has status = 'updated'"}))
    else:
        print(json.dumps({"test": "status_is_updated", "passed": False, "message": f"Expected status = 'updated', got status = '{status}'"}))
else:
    print(json.dumps({"test": "status_is_updated", "passed": False, "message": "state.json is not a JSON object (dict)"}))

# Test 4: answer.txt exists and contains "2"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "2":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains exactly '2'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '2' in answer.txt, got '{answer}'"}))
