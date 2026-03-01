#!/usr/bin/env python3
"""Verification script for Challenge 137: Concurrent Memory Writes"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: shared.json exists and is valid JSON
shared_path = os.path.join(SETUP_DIR, "shared.json")
if not os.path.exists(shared_path):
    print(json.dumps({"test": "shared_file_exists", "passed": False, "message": "shared.json does not exist"}))
    sys.exit(0)

try:
    with open(shared_path, "r") as f:
        shared = json.load(f)
    print(json.dumps({"test": "shared_file_exists", "passed": True, "message": "shared.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "shared_file_exists", "passed": False, "message": f"shared.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: shared.json contains agent_a entry
if isinstance(shared, dict) and "agent_a" in shared:
    agent_a = shared["agent_a"]
    if isinstance(agent_a, dict) and agent_a.get("status") == "done" and agent_a.get("result") == 42:
        print(json.dumps({"test": "agent_a_present", "passed": True, "message": "agent_a entry is correct (status=done, result=42)"}))
    else:
        print(json.dumps({"test": "agent_a_present", "passed": False, "message": f"agent_a has wrong data: {agent_a}"}))
else:
    print(json.dumps({"test": "agent_a_present", "passed": False, "message": "shared.json does not contain agent_a entry"}))

# Test 3: shared.json contains agent_b entry
if isinstance(shared, dict) and "agent_b" in shared:
    agent_b = shared["agent_b"]
    if isinstance(agent_b, dict) and agent_b.get("status") == "done" and agent_b.get("result") == 99:
        print(json.dumps({"test": "agent_b_present", "passed": True, "message": "agent_b entry is correct (status=done, result=99)"}))
    else:
        print(json.dumps({"test": "agent_b_present", "passed": False, "message": f"agent_b has wrong data: {agent_b}"}))
else:
    print(json.dumps({"test": "agent_b_present", "passed": False, "message": "shared.json does not contain agent_b entry (Agent B may have overwritten Agent A)"}))

# Test 4: Both agents coexist (neither was overwritten)
if isinstance(shared, dict) and "agent_a" in shared and "agent_b" in shared:
    print(json.dumps({"test": "both_agents_coexist", "passed": True, "message": "Both agent_a and agent_b coexist in shared.json"}))
else:
    present = [k for k in ("agent_a", "agent_b") if isinstance(shared, dict) and k in shared]
    print(json.dumps({"test": "both_agents_coexist", "passed": False, "message": f"Only these agent entries found: {present}"}))

# Test 5: answer.json exists and is valid JSON
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

# Test 6: answer.json has total=141
if isinstance(answer, dict) and answer.get("total") == 141:
    print(json.dumps({"test": "answer_total_correct", "passed": True, "message": "answer.json has total=141 (42 + 99)"}))
else:
    val = answer.get("total") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "answer_total_correct", "passed": False, "message": f"Expected total=141, got {val}"}))
