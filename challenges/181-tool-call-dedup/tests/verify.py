#!/usr/bin/env python3
"""Verify challenge 181: Tool Call Deduplication."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []

# Test 1: answer.txt exists
answer_path = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_path):
    results.append({"test": "answer_file_exists", "passed": True, "message": "answer.txt exists"})
else:
    results.append({"test": "answer_file_exists", "passed": False, "message": "answer.txt not found"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 2: answer.txt contains a valid number
with open(answer_path, "r") as f:
    content = f.read().strip()

try:
    answer_count = int(content)
    results.append({"test": "valid_number", "passed": True, "message": f"Answer is a valid number: {answer_count}"})
except ValueError:
    results.append({"test": "valid_number", "passed": False, "message": f"Answer is not a valid number: '{content}'"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 3: The answer matches the actual state count
state_path = os.path.join(CHALLENGE_DIR, "tools", ".counter_state.json")
if os.path.exists(state_path):
    with open(state_path, "r") as f:
        state = json.load(f)
    actual_count = state.get("count", 0)
    if answer_count == actual_count:
        results.append({"test": "count_matches_state", "passed": True, "message": f"Answer ({answer_count}) matches actual tool call count ({actual_count})"})
    else:
        results.append({"test": "count_matches_state", "passed": False, "message": f"Answer ({answer_count}) does not match actual tool call count ({actual_count})"})
else:
    results.append({"test": "count_matches_state", "passed": False, "message": "Tool state file not found - tool was never called"})

for r in results:
    print(json.dumps(r))
