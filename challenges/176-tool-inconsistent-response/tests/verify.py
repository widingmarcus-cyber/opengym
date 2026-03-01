#!/usr/bin/env python3
"""Verify challenge 176: Tool Inconsistent Response."""

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

# Test 2: answer.txt contains "42" (the mode value)
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "42":
    results.append({"test": "correct_mode_value", "passed": True, "message": "Correct mode value: 42"})
else:
    results.append({"test": "correct_mode_value", "passed": False, "message": f"Expected '42', got '{content}'"})

# Test 3: Tool was called at least 3 times (check state file)
state_path = os.path.join(CHALLENGE_DIR, "tools", ".flaky_state.json")
if os.path.exists(state_path):
    with open(state_path, "r") as f:
        state = json.load(f)
    call_count = state.get("call_count", 0)
    if call_count >= 3:
        results.append({"test": "multiple_calls_made", "passed": True, "message": f"Tool called {call_count} times (>= 3 required)"})
    else:
        results.append({"test": "multiple_calls_made", "passed": False, "message": f"Tool called only {call_count} times, need at least 3"})
else:
    results.append({"test": "multiple_calls_made", "passed": False, "message": "Tool state file not found - tool was never called"})

for r in results:
    print(json.dumps(r))
