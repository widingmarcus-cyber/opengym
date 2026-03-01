#!/usr/bin/env python3
"""Verification script for Challenge 152: Deadlock Detection (3-node)"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: resolution.json exists and is valid JSON
resolution_path = os.path.join(SETUP_DIR, "resolution.json")
if not os.path.exists(resolution_path):
    print(json.dumps({"test": "resolution_exists", "passed": False, "message": "resolution.json does not exist"}))
    sys.exit(0)

try:
    with open(resolution_path, "r") as f:
        resolution = json.load(f)
    print(json.dumps({"test": "resolution_exists", "passed": True, "message": "resolution.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "resolution_exists", "passed": False, "message": f"resolution.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: resolution.json has the correct cycle
if isinstance(resolution, dict) and "cycle" in resolution:
    cycle = resolution["cycle"]
    # The cycle should be ["A", "B", "C", "A"] or equivalent rotation
    if isinstance(cycle, list) and len(cycle) == 4:
        # Check it contains A, B, C and forms a valid cycle
        nodes_in_cycle = set(cycle[:3])
        if nodes_in_cycle == {"A", "B", "C"} and cycle[0] == cycle[3]:
            print(json.dumps({"test": "cycle_correct", "passed": True, "message": f"Correct cycle detected: {cycle}"}))
        else:
            print(json.dumps({"test": "cycle_correct", "passed": False, "message": f"Cycle should be [A, B, C, A] (or rotation). Got: {cycle}"}))
    else:
        print(json.dumps({"test": "cycle_correct", "passed": False, "message": f"Cycle should have 4 elements (3 nodes + return). Got: {cycle}"}))
else:
    print(json.dumps({"test": "cycle_correct", "passed": False, "message": f"resolution.json does not contain a 'cycle' field: {resolution}"}))

# Test 3: resolution.json has a break_at field
if isinstance(resolution, dict) and "break_at" in resolution:
    break_at = resolution["break_at"]
    if break_at in ("A", "B", "C"):
        print(json.dumps({"test": "break_at_valid", "passed": True, "message": f"break_at is valid: '{break_at}'"}))
    else:
        print(json.dumps({"test": "break_at_valid", "passed": False, "message": f"break_at should be A, B, or C. Got: '{break_at}'"}))
else:
    print(json.dumps({"test": "break_at_valid", "passed": False, "message": "resolution.json does not contain a 'break_at' field"}))

# Test 4: answer.txt exists and equals "CYCLE_BROKEN"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "CYCLE_BROKEN":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt correctly contains 'CYCLE_BROKEN'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'CYCLE_BROKEN', got '{answer}'"}))
