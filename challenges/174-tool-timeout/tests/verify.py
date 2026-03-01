#!/usr/bin/env python3
"""Verification script for Challenge 174: Tool Timeout."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct fallback value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "fallback_value":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'fallback_value'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'fallback_value', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: tool was called at least twice (timeout detected, then fallback used)
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "hang_state.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    count = state.get("count", 0)
    if count >= 2:
        results.append({"test": "timeout_handled", "passed": True, "message": f"Tool was called {count} times — timeout was detected and fallback was used"})
    elif count == 1:
        results.append({"test": "timeout_handled", "passed": True, "message": "Tool was called once with --fallback directly (agent read docs first)"})
    else:
        results.append({"test": "timeout_handled", "passed": False, "message": "Tool was never called"})
else:
    results.append({"test": "timeout_handled", "passed": False, "message": "State file not found — tool was never called"})

for r in results:
    print(json.dumps(r))
