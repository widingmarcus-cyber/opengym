#!/usr/bin/env python3
"""Verification script for Challenge 148: File Write Race"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: output.json exists and is valid JSON
output_path = os.path.join(SETUP_DIR, "output.json")
if not os.path.exists(output_path):
    print(json.dumps({"test": "output_file_exists", "passed": False, "message": "output.json does not exist"}))
    sys.exit(0)

try:
    with open(output_path, "r") as f:
        output = json.load(f)
    print(json.dumps({"test": "output_file_exists", "passed": True, "message": "output.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "output_file_exists", "passed": False, "message": f"output.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: output.json contains agent_a entry with correct data
if isinstance(output, dict) and "agent_a" in output:
    agent_a = output["agent_a"]
    if isinstance(agent_a, dict) and agent_a.get("agent_a_data") == [1, 2, 3]:
        print(json.dumps({"test": "agent_a_present", "passed": True, "message": "agent_a entry is correct with data [1, 2, 3]"}))
    else:
        print(json.dumps({"test": "agent_a_present", "passed": False, "message": f"agent_a has wrong data: {agent_a}"}))
else:
    print(json.dumps({"test": "agent_a_present", "passed": False, "message": "output.json does not contain agent_a entry"}))

# Test 3: output.json contains agent_b entry with correct data
if isinstance(output, dict) and "agent_b" in output:
    agent_b = output["agent_b"]
    if isinstance(agent_b, dict) and agent_b.get("agent_b_data") == [4, 5, 6]:
        print(json.dumps({"test": "agent_b_present", "passed": True, "message": "agent_b entry is correct with data [4, 5, 6]"}))
    else:
        print(json.dumps({"test": "agent_b_present", "passed": False, "message": f"agent_b has wrong data: {agent_b}"}))
else:
    print(json.dumps({"test": "agent_b_present", "passed": False, "message": "output.json does not contain agent_b entry (Agent B may have overwritten Agent A)"}))

# Test 4: Both agents coexist
if isinstance(output, dict) and "agent_a" in output and "agent_b" in output:
    print(json.dumps({"test": "both_agents_coexist", "passed": True, "message": "Both agent_a and agent_b coexist in output.json"}))
else:
    present = [k for k in ("agent_a", "agent_b") if isinstance(output, dict) and k in output]
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

# Test 6: answer.json has merged=true
if isinstance(answer, dict) and answer.get("merged") is True:
    print(json.dumps({"test": "answer_merged", "passed": True, "message": "answer.json has merged=true"}))
else:
    val = answer.get("merged") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "answer_merged", "passed": False, "message": f"Expected merged=true, got {val}"}))

# Test 7: answer.json has total_items=6
if isinstance(answer, dict) and answer.get("total_items") == 6:
    print(json.dumps({"test": "answer_total_items", "passed": True, "message": "answer.json has total_items=6"}))
else:
    val = answer.get("total_items") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "answer_total_items", "passed": False, "message": f"Expected total_items=6, got {val}"}))
