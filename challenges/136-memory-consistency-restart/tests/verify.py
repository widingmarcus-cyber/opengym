#!/usr/bin/env python3
"""Verification script for Challenge 136: Memory Consistency After Restart"""
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

# Test 2: state.json has initialized=true
if isinstance(state, dict) and state.get("initialized") is True:
    print(json.dumps({"test": "state_initialized", "passed": True, "message": "state.json has initialized=true"}))
else:
    val = state.get("initialized") if isinstance(state, dict) else None
    print(json.dumps({"test": "state_initialized", "passed": False, "message": f"Expected initialized=true, got {val}"}))

# Test 3: state.json has count=2
if isinstance(state, dict) and state.get("count") == 2:
    print(json.dumps({"test": "state_count", "passed": True, "message": "state.json has count=2"}))
else:
    val = state.get("count") if isinstance(state, dict) else None
    print(json.dumps({"test": "state_count", "passed": False, "message": f"Expected count=2, got {val}"}))

# Test 4: state.json has items=["apple", "banana"]
expected_items = ["apple", "banana"]
if isinstance(state, dict) and state.get("items") == expected_items:
    print(json.dumps({"test": "state_items", "passed": True, "message": "state.json has items=['apple', 'banana']"}))
else:
    val = state.get("items") if isinstance(state, dict) else None
    print(json.dumps({"test": "state_items", "passed": False, "message": f"Expected items={expected_items}, got {val}"}))

# Test 5: answer.json exists and is valid JSON
answer_path = os.path.join(SETUP_DIR, "answer.json")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_file_exists", "passed": False, "message": "answer.json does not exist"}))
    sys.exit(0)

try:
    with open(answer_path, "r") as f:
        answer = json.load(f)
    print(json.dumps({"test": "answer_file_exists", "passed": True, "message": "answer.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answer_file_exists", "passed": False, "message": f"answer.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 6: answer.json matches the expected final state
expected_state = {"initialized": True, "count": 2, "items": ["apple", "banana"]}
if isinstance(answer, dict) and answer.get("initialized") is True and answer.get("count") == 2 and answer.get("items") == expected_items:
    print(json.dumps({"test": "answer_matches_state", "passed": True, "message": "answer.json contains the correct final state"}))
else:
    print(json.dumps({"test": "answer_matches_state", "passed": False, "message": f"answer.json does not match expected state. Got: {answer}"}))

# Test 7: state.json and answer.json are consistent
if state == answer:
    print(json.dumps({"test": "state_answer_consistent", "passed": True, "message": "state.json and answer.json are consistent"}))
else:
    print(json.dumps({"test": "state_answer_consistent", "passed": False, "message": "state.json and answer.json do not match each other"}))
