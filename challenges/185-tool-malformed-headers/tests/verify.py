#!/usr/bin/env python3
"""Verify challenge 185: Tool Malformed Headers."""

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

# Test 2: answer.txt contains "valid_result_88"
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "valid_result_88":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data extracted: valid_result_88"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'valid_result_88', got '{content}'"})

# Test 3: Agent did not include WARNING lines in the answer
if "WARNING" not in content:
    results.append({"test": "no_warnings_in_answer", "passed": True, "message": "Answer does not contain warning text"})
else:
    results.append({"test": "no_warnings_in_answer", "passed": False, "message": "Answer contains WARNING text that should have been filtered"})

for r in results:
    print(json.dumps(r))
