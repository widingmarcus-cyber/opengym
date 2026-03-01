#!/usr/bin/env python3
"""Verification script for Challenge 149: Distributed Lock"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: resource.txt exists
resource_path = os.path.join(SETUP_DIR, "resource.txt")
if not os.path.exists(resource_path):
    print(json.dumps({"test": "resource_file_exists", "passed": False, "message": "resource.txt does not exist"}))
    sys.exit(0)

with open(resource_path, "r") as f:
    resource_content = f.read()
resource_lines = [line.strip() for line in resource_content.strip().splitlines() if line.strip()]
print(json.dumps({"test": "resource_file_exists", "passed": True, "message": "resource.txt exists"}))

# Test 2: resource.txt contains AGENT_A_WAS_HERE
if "AGENT_A_WAS_HERE" in resource_lines:
    print(json.dumps({"test": "agent_a_wrote", "passed": True, "message": "resource.txt contains AGENT_A_WAS_HERE"}))
else:
    print(json.dumps({"test": "agent_a_wrote", "passed": False, "message": f"resource.txt does not contain AGENT_A_WAS_HERE. Lines: {resource_lines}"}))

# Test 3: resource.txt contains AGENT_B_WAS_HERE
if "AGENT_B_WAS_HERE" in resource_lines:
    print(json.dumps({"test": "agent_b_wrote", "passed": True, "message": "resource.txt contains AGENT_B_WAS_HERE"}))
else:
    print(json.dumps({"test": "agent_b_wrote", "passed": False, "message": f"resource.txt does not contain AGENT_B_WAS_HERE. Lines: {resource_lines}"}))

# Test 4: resource.txt has exactly 2 lines
if len(resource_lines) == 2:
    print(json.dumps({"test": "resource_line_count", "passed": True, "message": "resource.txt has exactly 2 lines"}))
else:
    print(json.dumps({"test": "resource_line_count", "passed": False, "message": f"Expected 2 lines, got {len(resource_lines)}"}))

# Test 5: lock.json has locked=false (lock released)
lock_path = os.path.join(SETUP_DIR, "lock.json")
if not os.path.exists(lock_path):
    print(json.dumps({"test": "lock_released", "passed": False, "message": "lock.json does not exist"}))
else:
    try:
        with open(lock_path, "r") as f:
            lock = json.load(f)
        if isinstance(lock, dict) and lock.get("locked") is False:
            print(json.dumps({"test": "lock_released", "passed": True, "message": "lock.json has locked=false (lock properly released)"}))
        else:
            print(json.dumps({"test": "lock_released", "passed": False, "message": f"Lock not released. lock.json: {lock}"}))
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "lock_released", "passed": False, "message": f"lock.json is not valid JSON: {e}"}))

# Test 6: answer.txt exists and equals "2"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "2":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt correctly contains '2'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '2', got '{answer}'"}))
