#!/usr/bin/env python3
"""Verification script for Challenge 170: Tool Output Type Change."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "42":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains '42'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected '42', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: Verify value is parseable as integer (not quoted string)
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    # Check it's not wrapped in quotes
    if answer.startswith('"') or answer.startswith("'"):
        results.append({"test": "type_correct", "passed": False, "message": f"Value appears to be a quoted string: {answer}"})
    else:
        try:
            val = int(answer)
            if val == 42:
                results.append({"test": "type_correct", "passed": True, "message": "Value correctly parsed as integer 42"})
            else:
                results.append({"test": "type_correct", "passed": False, "message": f"Integer value is {val}, expected 42"})
        except ValueError:
            results.append({"test": "type_correct", "passed": False, "message": f"Value '{answer}' could not be parsed as integer"})
else:
    results.append({"test": "type_correct", "passed": False, "message": "answer.txt not found"})

for r in results:
    print(json.dumps(r))
