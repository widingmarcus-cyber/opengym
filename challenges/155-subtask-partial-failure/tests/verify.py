#!/usr/bin/env python3
"""Verification script for Challenge 155: Subtask Partial Failure Propagation"""
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

# Test 2: results.json has exactly 5 entries
if isinstance(results, list) and len(results) == 5:
    print(json.dumps({"test": "results_count", "passed": True, "message": "results.json has exactly 5 entries"}))
else:
    count = len(results) if isinstance(results, list) else "not a list"
    print(json.dumps({"test": "results_count", "passed": False, "message": f"Expected 5 entries, got {count}"}))

# Test 3: Subtask 3 (input=-1) has status="failed"
if isinstance(results, list):
    task_3 = None
    for r in results:
        if isinstance(r, dict) and r.get("id") == 3:
            task_3 = r
            break
    if task_3 is not None:
        if task_3.get("status") == "failed":
            print(json.dumps({"test": "task_3_failed", "passed": True, "message": "Subtask 3 correctly marked as failed (negative input)"}))
        else:
            print(json.dumps({"test": "task_3_failed", "passed": False, "message": f"Subtask 3 should be 'failed', got status='{task_3.get('status')}'"}))
    else:
        print(json.dumps({"test": "task_3_failed", "passed": False, "message": "Subtask 3 not found in results"}))
else:
    print(json.dumps({"test": "task_3_failed", "passed": False, "message": "results.json is not a list"}))

# Test 4: Successful subtasks have correct squared values
expected_outputs = {1: 100, 2: 400, 4: 1600, 5: 2500}
if isinstance(results, list):
    all_correct = True
    errors = []
    for r in results:
        if isinstance(r, dict) and r.get("id") in expected_outputs:
            task_id = r["id"]
            expected = expected_outputs[task_id]
            if r.get("status") != "success":
                all_correct = False
                errors.append(f"Task {task_id}: expected status='success', got '{r.get('status')}'")
            elif r.get("output") != expected:
                all_correct = False
                errors.append(f"Task {task_id}: expected output={expected}, got {r.get('output')}")
    if all_correct:
        print(json.dumps({"test": "success_outputs_correct", "passed": True, "message": "All successful subtasks have correct squared outputs"}))
    else:
        print(json.dumps({"test": "success_outputs_correct", "passed": False, "message": f"Incorrect outputs: {'; '.join(errors)}"}))
else:
    print(json.dumps({"test": "success_outputs_correct", "passed": False, "message": "results.json is not a list"}))

# Test 5: answer.json exists and is valid JSON
answer_path = os.path.join(SETUP_DIR, "answer.json")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_exists", "passed": False, "message": "answer.json does not exist"}))
    sys.exit(0)

try:
    with open(answer_path, "r") as f:
        answer = json.load(f)
    print(json.dumps({"test": "answer_exists", "passed": True, "message": "answer.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answer_exists", "passed": False, "message": f"answer.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 6: answer.json has total_succeeded=4
if isinstance(answer, dict) and answer.get("total_succeeded") == 4:
    print(json.dumps({"test": "total_succeeded", "passed": True, "message": "answer.json has total_succeeded=4"}))
else:
    val = answer.get("total_succeeded") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "total_succeeded", "passed": False, "message": f"Expected total_succeeded=4, got {val}"}))

# Test 7: answer.json has total_failed=1
if isinstance(answer, dict) and answer.get("total_failed") == 1:
    print(json.dumps({"test": "total_failed", "passed": True, "message": "answer.json has total_failed=1"}))
else:
    val = answer.get("total_failed") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "total_failed", "passed": False, "message": f"Expected total_failed=1, got {val}"}))

# Test 8: answer.json has failed_ids=[3]
if isinstance(answer, dict) and answer.get("failed_ids") == [3]:
    print(json.dumps({"test": "failed_ids_correct", "passed": True, "message": "answer.json has failed_ids=[3]"}))
else:
    val = answer.get("failed_ids") if isinstance(answer, dict) else answer
    print(json.dumps({"test": "failed_ids_correct", "passed": False, "message": f"Expected failed_ids=[3], got {val}"}))
