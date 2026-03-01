#!/usr/bin/env python3
"""Verification script for Challenge 166: 429 Retry-After Enforcement."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "success_data_42":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'success_data_42'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'success_data_42', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: call_count.json shows 3+ calls were made
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "call_count.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    call_count = state.get("count", 0)
    if call_count >= 3:
        results.append({"test": "retry_count", "passed": True, "message": f"Tool was called {call_count} times (>=3 required)"})
    else:
        results.append({"test": "retry_count", "passed": False, "message": f"Tool was only called {call_count} times, expected >=3"})
else:
    results.append({"test": "retry_count", "passed": False, "message": "State file not found — tool was never called"})

for r in results:
    print(json.dumps(r))
