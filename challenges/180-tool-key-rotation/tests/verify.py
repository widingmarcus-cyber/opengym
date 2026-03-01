#!/usr/bin/env python3
"""Verify challenge 180: Tool Key Rotation."""

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

# Test 2: answer.txt contains "classified_info_55"
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "classified_info_55":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data retrieved: classified_info_55"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'classified_info_55', got '{content}'"})

# Test 3: keys.json still intact
keys_path = os.path.join(CHALLENGE_DIR, "setup", "keys.json")
if os.path.exists(keys_path):
    with open(keys_path, "r") as f:
        keys = json.load(f)
    if "rotated" in keys and keys["rotated"] == "key_v2":
        results.append({"test": "keys_intact", "passed": True, "message": "keys.json is intact with correct rotated key"})
    else:
        results.append({"test": "keys_intact", "passed": False, "message": "keys.json is missing or has wrong rotated key"})
else:
    results.append({"test": "keys_intact", "passed": False, "message": "keys.json not found"})

for r in results:
    print(json.dumps(r))
