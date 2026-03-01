#!/usr/bin/env python3
"""Verification script for Challenge 154: Task Idempotency"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: results.json exists and is valid JSON
results_path = os.path.join(SETUP_DIR, "results.json")
if not os.path.exists(results_path):
    print(json.dumps({"test": "results_exists", "passed": False, "message": "results.json does not exist"}))
    sys.exit(0)

try:
    with open(results_path, "r") as f:
        results = json.load(f)
    print(json.dumps({"test": "results_exists", "passed": True, "message": "results.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "results_exists", "passed": False, "message": f"results.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: counter equals 2 (not 3 -- duplicate was skipped)
if isinstance(results, dict) and results.get("counter") == 2:
    print(json.dumps({"test": "counter_correct", "passed": True, "message": "Counter is 2 (duplicate task was correctly skipped)"}))
elif isinstance(results, dict) and results.get("counter") == 3:
    print(json.dumps({"test": "counter_correct", "passed": False, "message": "Counter is 3 -- duplicate task was NOT skipped (should be 2)"}))
else:
    val = results.get("counter") if isinstance(results, dict) else results
    print(json.dumps({"test": "counter_correct", "passed": False, "message": f"Expected counter=2, got {val}"}))

# Test 3: processed.json exists and is valid JSON
processed_path = os.path.join(SETUP_DIR, "processed.json")
if not os.path.exists(processed_path):
    print(json.dumps({"test": "processed_exists", "passed": False, "message": "processed.json does not exist"}))
    sys.exit(0)

try:
    with open(processed_path, "r") as f:
        processed = json.load(f)
    print(json.dumps({"test": "processed_exists", "passed": True, "message": "processed.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "processed_exists", "passed": False, "message": f"processed.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 4: processed.json contains task_001
if isinstance(processed, list) and "task_001" in processed:
    print(json.dumps({"test": "task_001_recorded", "passed": True, "message": "task_001 is recorded in processed.json"}))
else:
    print(json.dumps({"test": "task_001_recorded", "passed": False, "message": f"task_001 not found in processed.json: {processed}"}))

# Test 5: processed.json contains task_002
if isinstance(processed, list) and "task_002" in processed:
    print(json.dumps({"test": "task_002_recorded", "passed": True, "message": "task_002 is recorded in processed.json"}))
else:
    print(json.dumps({"test": "task_002_recorded", "passed": False, "message": f"task_002 not found in processed.json: {processed}"}))

# Test 6: processed.json has exactly 2 entries (no duplicate task_001)
if isinstance(processed, list) and len(processed) == 2:
    print(json.dumps({"test": "no_duplicate_processing", "passed": True, "message": "Exactly 2 tasks in processed list (no duplicates)"}))
elif isinstance(processed, list) and processed.count("task_001") > 1:
    print(json.dumps({"test": "no_duplicate_processing", "passed": False, "message": f"task_001 appears {processed.count('task_001')} times -- should only appear once"}))
else:
    print(json.dumps({"test": "no_duplicate_processing", "passed": False, "message": f"Expected 2 entries, got {len(processed) if isinstance(processed, list) else processed}"}))

# Test 7: answer.txt exists and equals "2"
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
