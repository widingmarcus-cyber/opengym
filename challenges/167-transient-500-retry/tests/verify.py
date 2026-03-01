#!/usr/bin/env python3
"""Verification script for Challenge 167: Transient 500 Retry."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "recovered_result":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'recovered_result'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'recovered_result', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: attempts.json shows at least 2 calls
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "attempts.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    attempts = state.get("attempts", 0)
    if attempts >= 2:
        results.append({"test": "retry_attempted", "passed": True, "message": f"Service was called {attempts} times (>=2 required)"})
    else:
        results.append({"test": "retry_attempted", "passed": False, "message": f"Service was only called {attempts} time, expected >=2"})
else:
    results.append({"test": "retry_attempted", "passed": False, "message": "State file not found — service was never called"})

for r in results:
    print(json.dumps(r))
