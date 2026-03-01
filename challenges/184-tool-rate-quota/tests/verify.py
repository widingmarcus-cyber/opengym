#!/usr/bin/env python3
"""Verify challenge 184: Tool Rate Quota Exhaustion."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []

# Test 1: answer.json exists
answer_path = os.path.join(CHALLENGE_DIR, "setup", "answer.json")
if os.path.exists(answer_path):
    results.append({"test": "answer_file_exists", "passed": True, "message": "answer.json exists"})
else:
    results.append({"test": "answer_file_exists", "passed": False, "message": "answer.json not found"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 2: answer.json contains valid JSON with 8 results
try:
    with open(answer_path, "r") as f:
        answer = json.load(f)
    results.append({"test": "valid_json", "passed": True, "message": "answer.json contains valid JSON"})
except (json.JSONDecodeError, ValueError) as e:
    results.append({"test": "valid_json", "passed": False, "message": f"answer.json is not valid JSON: {e}"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 3: Has all 8 results
expected_keys = {"q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"}
actual_keys = set(answer.keys())
if expected_keys.issubset(actual_keys):
    results.append({"test": "all_eight_results", "passed": True, "message": f"All 8 query results present"})
else:
    missing = expected_keys - actual_keys
    results.append({"test": "all_eight_results", "passed": False, "message": f"Missing query results: {missing}"})

# Test 4: Results are correct
expected_results = {f"q{i}": f"r{i}" for i in range(1, 9)}
all_correct = True
wrong = []
for key, expected_val in expected_results.items():
    if key in answer and answer[key] != expected_val:
        all_correct = False
        wrong.append(f"{key}: expected '{expected_val}', got '{answer[key]}'")

if all_correct:
    results.append({"test": "correct_results", "passed": True, "message": "All query results are correct"})
else:
    results.append({"test": "correct_results", "passed": False, "message": f"Wrong results: {'; '.join(wrong)}"})

# Test 5: Quota was respected (5 or fewer calls)
state_path = os.path.join(CHALLENGE_DIR, "tools", ".quota_state.json")
if os.path.exists(state_path):
    with open(state_path, "r") as f:
        state = json.load(f)
    call_count = state.get("call_count", 0)
    if call_count <= 5:
        results.append({"test": "quota_respected", "passed": True, "message": f"Quota respected: {call_count} calls made (limit: 5)"})
    else:
        results.append({"test": "quota_respected", "passed": False, "message": f"Quota exceeded: {call_count} calls made (limit: 5)"})
else:
    results.append({"test": "quota_respected", "passed": False, "message": "Tool state file not found - tool was never called"})

for r in results:
    print(json.dumps(r))
