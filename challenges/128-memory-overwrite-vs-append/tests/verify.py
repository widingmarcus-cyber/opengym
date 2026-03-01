#!/usr/bin/env python3
"""Verification script for Challenge 128: Memory Overwrite vs Append"""
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
        raw_content = f.read()
    memory = json.loads(raw_content)
    print(json.dumps({"test": "memory_file_exists", "passed": True, "message": "memory.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "memory_file_exists", "passed": False, "message": f"memory.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: memory.json has exactly one "color" key with value "red"
if isinstance(memory, dict):
    if "color" in memory:
        if memory["color"] == "red":
            print(json.dumps({"test": "color_is_red", "passed": True, "message": "memory.json has color = red"}))
        else:
            print(json.dumps({"test": "color_is_red", "passed": False, "message": f"Expected color = 'red', got '{memory['color']}'"}))
    else:
        print(json.dumps({"test": "color_is_red", "passed": False, "message": "memory.json does not contain key 'color'"}))
else:
    print(json.dumps({"test": "color_is_red", "passed": False, "message": "memory.json is not a JSON object (dict)"}))

# Test 3: No duplicate "color" keys (check raw content for duplicate keys)
color_count = raw_content.count('"color"')
if color_count == 1:
    print(json.dumps({"test": "no_duplicate_keys", "passed": True, "message": "Only one 'color' key found in memory.json"}))
else:
    print(json.dumps({"test": "no_duplicate_keys", "passed": False, "message": f"Found {color_count} occurrences of 'color' key in memory.json (expected 1)"}))

# Test 4: answer.txt exists and contains "red"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "red":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains exactly 'red'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'red' in answer.txt, got '{answer}'"}))
