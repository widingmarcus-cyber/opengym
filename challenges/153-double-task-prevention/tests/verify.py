#!/usr/bin/env python3
"""Verification script for Challenge 153: Double Task Assignment Prevention"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: task_registry.json exists and is valid JSON
registry_path = os.path.join(SETUP_DIR, "task_registry.json")
if not os.path.exists(registry_path):
    print(json.dumps({"test": "registry_exists", "passed": False, "message": "task_registry.json does not exist"}))
    sys.exit(0)

try:
    with open(registry_path, "r") as f:
        registry = json.load(f)
    print(json.dumps({"test": "registry_exists", "passed": True, "message": "task_registry.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "registry_exists", "passed": False, "message": f"task_registry.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: agent_a has tasks 1, 2, 3
if isinstance(registry, dict) and "agent_a" in registry:
    agent_a_tasks = registry["agent_a"]
    if isinstance(agent_a_tasks, list) and sorted(agent_a_tasks) == [1, 2, 3]:
        print(json.dumps({"test": "agent_a_tasks", "passed": True, "message": "agent_a has tasks [1, 2, 3]"}))
    else:
        print(json.dumps({"test": "agent_a_tasks", "passed": False, "message": f"agent_a should have [1, 2, 3], got {agent_a_tasks}"}))
else:
    print(json.dumps({"test": "agent_a_tasks", "passed": False, "message": "task_registry.json does not contain agent_a entry"}))

# Test 3: agent_b has tasks 4, 5
if isinstance(registry, dict) and "agent_b" in registry:
    agent_b_tasks = registry["agent_b"]
    if isinstance(agent_b_tasks, list) and sorted(agent_b_tasks) == [4, 5]:
        print(json.dumps({"test": "agent_b_tasks", "passed": True, "message": "agent_b has tasks [4, 5]"}))
    else:
        print(json.dumps({"test": "agent_b_tasks", "passed": False, "message": f"agent_b should have [4, 5], got {agent_b_tasks}"}))
else:
    print(json.dumps({"test": "agent_b_tasks", "passed": False, "message": "task_registry.json does not contain agent_b entry"}))

# Test 4: No duplicate task IDs across agents
if isinstance(registry, dict):
    all_task_ids = []
    for agent, tasks in registry.items():
        if isinstance(tasks, list):
            all_task_ids.extend(tasks)
    duplicates = len(all_task_ids) - len(set(all_task_ids))
    if duplicates == 0:
        print(json.dumps({"test": "no_duplicates", "passed": True, "message": f"No duplicate task IDs found. All {len(all_task_ids)} assignments are unique"}))
    else:
        print(json.dumps({"test": "no_duplicates", "passed": False, "message": f"Found {duplicates} duplicate task ID(s). All IDs: {all_task_ids}"}))
else:
    print(json.dumps({"test": "no_duplicates", "passed": False, "message": "task_registry.json is not a valid dict"}))

# Test 5: All 5 tasks are assigned
if isinstance(registry, dict):
    all_task_ids = []
    for agent, tasks in registry.items():
        if isinstance(tasks, list):
            all_task_ids.extend(tasks)
    if sorted(set(all_task_ids)) == [1, 2, 3, 4, 5]:
        print(json.dumps({"test": "all_tasks_assigned", "passed": True, "message": "All 5 tasks (1-5) are assigned"}))
    else:
        print(json.dumps({"test": "all_tasks_assigned", "passed": False, "message": f"Not all tasks assigned. Found: {sorted(set(all_task_ids))}"}))

# Test 6: answer.json exists and is correct
answer_path = os.path.join(SETUP_DIR, "answer.json")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.json does not exist"}))
    sys.exit(0)

try:
    with open(answer_path, "r") as f:
        answer = json.load(f)
    if isinstance(answer, dict) and answer.get("total_assigned") == 5 and answer.get("duplicates") == 0:
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.json has total_assigned=5, duplicates=0"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected total_assigned=5, duplicates=0. Got: {answer}"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"answer.json is not valid JSON: {e}"}))
