#!/usr/bin/env python3
"""Verify challenge 179: Tool Auth Refresh."""

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

# Test 2: answer.txt contains "secret_data_99"
with open(answer_path, "r") as f:
    answer_content = f.read().strip()

if answer_content == "secret_data_99":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data retrieved: secret_data_99"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'secret_data_99', got '{answer_content}'"})

# Test 3: token.txt updated to fresh token
token_path = os.path.join(CHALLENGE_DIR, "setup", "token.txt")
if os.path.exists(token_path):
    with open(token_path, "r") as f:
        token_content = f.read().strip()
    if token_content == "fresh_token_xyz":
        results.append({"test": "token_updated", "passed": True, "message": "Token updated to fresh_token_xyz"})
    else:
        results.append({"test": "token_updated", "passed": False, "message": f"Expected token 'fresh_token_xyz', got '{token_content}'"})
else:
    results.append({"test": "token_updated", "passed": False, "message": "token.txt not found"})

for r in results:
    print(json.dumps(r))
