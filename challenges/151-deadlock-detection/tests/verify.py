#!/usr/bin/env python3
"""Verification script for Challenge 151: Deadlock Detection (2-node)"""
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

# Test 2: resolution.json describes the cycle
if isinstance(resolution, dict) and "cycle" in resolution:
    cycle = resolution["cycle"]
    # Check that cycle mentions both agent_a and agent_b
    has_a = "agent_a" in cycle or "A" in cycle
    has_b = "agent_b" in cycle or "B" in cycle
    if has_a and has_b:
        print(json.dumps({"test": "cycle_described", "passed": True, "message": f"Resolution describes the cycle involving both agents: {cycle}"}))
    else:
        print(json.dumps({"test": "cycle_described", "passed": False, "message": f"Cycle does not mention both agents: {cycle}"}))
elif isinstance(resolution, dict) and "cycle_detected" in resolution:
    print(json.dumps({"test": "cycle_described", "passed": True, "message": "Resolution acknowledges cycle detection"}))
else:
    print(json.dumps({"test": "cycle_described", "passed": False, "message": f"resolution.json does not describe a cycle: {resolution}"}))

# Test 3: agent_a_output.txt exists (cycle was broken)
output_path = os.path.join(SETUP_DIR, "agent_a_output.txt")
if os.path.exists(output_path):
    with open(output_path, "r") as f:
        content = f.read().strip()
    if content:
        print(json.dumps({"test": "cycle_broken", "passed": True, "message": f"agent_a_output.txt exists with content: '{content}'"}))
    else:
        print(json.dumps({"test": "cycle_broken", "passed": False, "message": "agent_a_output.txt exists but is empty"}))
else:
    print(json.dumps({"test": "cycle_broken", "passed": False, "message": "agent_a_output.txt does not exist -- cycle was not broken"}))

# Test 4: answer.txt exists and equals "DEADLOCK_RESOLVED"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "DEADLOCK_RESOLVED":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt correctly contains 'DEADLOCK_RESOLVED'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'DEADLOCK_RESOLVED', got '{answer}'"}))
