#!/usr/bin/env python3
"""Verification script for Challenge 133: Memory Compaction"""
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

# Test 2: memory.json has exactly 10 keys
key_count = len(memory) if isinstance(memory, dict) else -1
if key_count == 10:
    print(json.dumps({"test": "key_count_is_10", "passed": True, "message": "memory.json has exactly 10 keys"}))
else:
    print(json.dumps({"test": "key_count_is_10", "passed": False, "message": f"Expected 10 keys, found {key_count}"}))

# Test 3: All 10 keys are correct multiples of 100
expected_keys = {f"key_{i}" for i in range(100, 1001, 100)}
if isinstance(memory, dict):
    actual_keys = set(memory.keys())
    if actual_keys == expected_keys:
        print(json.dumps({"test": "correct_keys", "passed": True, "message": "All 10 keys are correct multiples of 100 (key_100 through key_1000)"}))
    else:
        missing = expected_keys - actual_keys
        extra = actual_keys - expected_keys
        msg = ""
        if missing:
            msg += f"Missing: {sorted(missing)}. "
        if extra:
            msg += f"Extra: {sorted(extra)}."
        print(json.dumps({"test": "correct_keys", "passed": False, "message": msg.strip()}))
else:
    print(json.dumps({"test": "correct_keys", "passed": False, "message": "memory.json is not a JSON object"}))

# Test 4: Values are correct for the retained keys
if isinstance(memory, dict):
    all_values_correct = True
    bad_values = []
    for i in range(100, 1001, 100):
        key = f"key_{i}"
        expected_value = f"value_{i:03d}"
        if key in memory and memory[key] != expected_value:
            all_values_correct = False
            bad_values.append(f"{key}: expected '{expected_value}', got '{memory[key]}'")
    if all_values_correct:
        print(json.dumps({"test": "correct_values", "passed": True, "message": "All retained keys have correct values"}))
    else:
        print(json.dumps({"test": "correct_values", "passed": False, "message": f"Incorrect values: {'; '.join(bad_values)}"}))
else:
    print(json.dumps({"test": "correct_values", "passed": False, "message": "memory.json is not a JSON object"}))

# Test 5: answer.txt exists and contains "10"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "10":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains exactly '10'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '10' in answer.txt, got '{answer}'"}))
