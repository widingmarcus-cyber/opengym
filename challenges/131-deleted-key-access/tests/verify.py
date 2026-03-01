#!/usr/bin/env python3
"""Verification script for Challenge 131: Deleted Key Access"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: memory.json exists and is valid JSON
memory_path = os.path.join(SETUP_DIR, "memory.json")
if not os.path.exists(memory_path):
    print(json.dumps({"test": "memory_file_exists", "passed": False, "message": "memory.json does not exist"}))
    sys.exit(0)

try:
    with open(memory_path, "r") as f:
        memory = json.load(f)
    print(json.dumps({"test": "memory_file_exists", "passed": True, "message": "memory.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "memory_file_exists", "passed": False, "message": f"memory.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: memory.json does NOT contain temp_token
if isinstance(memory, dict):
    if "temp_token" not in memory:
        print(json.dumps({"test": "temp_token_deleted", "passed": True, "message": "temp_token has been removed from memory.json"}))
    else:
        print(json.dumps({"test": "temp_token_deleted", "passed": False, "message": "temp_token still exists in memory.json (should have been deleted)"}))
else:
    print(json.dumps({"test": "temp_token_deleted", "passed": False, "message": "memory.json is not a JSON object (dict)"}))

# Test 3: memory.json still has name and role with correct values
if isinstance(memory, dict):
    errors = []
    if memory.get("name") != "Alice":
        errors.append(f"Expected name = 'Alice', got '{memory.get('name')}'")
    if memory.get("role") != "admin":
        errors.append(f"Expected role = 'admin', got '{memory.get('role')}'")
    if not errors:
        print(json.dumps({"test": "remaining_keys_intact", "passed": True, "message": "name and role preserved with correct values in memory.json"}))
    else:
        print(json.dumps({"test": "remaining_keys_intact", "passed": False, "message": "; ".join(errors)}))
else:
    print(json.dumps({"test": "remaining_keys_intact", "passed": False, "message": "memory.json is not a JSON object (dict)"}))

# Test 4: answer.json exists and is valid JSON
answer_path = os.path.join(SETUP_DIR, "answer.json")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_file_exists", "passed": False, "message": "answer.json does not exist"}))
    sys.exit(0)

try:
    with open(answer_path, "r") as f:
        answer = json.load(f)
    print(json.dumps({"test": "answer_file_exists", "passed": True, "message": "answer.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answer_file_exists", "passed": False, "message": f"answer.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 5: answer.json has name and role but NOT temp_token
if isinstance(answer, dict):
    errors = []
    if answer.get("name") != "Alice":
        errors.append(f"Expected name = 'Alice', got '{answer.get('name')}'")
    if answer.get("role") != "admin":
        errors.append(f"Expected role = 'admin', got '{answer.get('role')}'")
    if "temp_token" in answer:
        errors.append("temp_token found in answer.json (must NOT be included)")
    if not errors:
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.json has name and role, does not include temp_token"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": "; ".join(errors)}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.json is not a JSON object (dict)"}))
