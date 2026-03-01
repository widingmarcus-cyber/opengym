#!/usr/bin/env python3
"""Verification script for Challenge 104: Selective Memory"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

EXPECTED_PROJECTS = {
    "Project Falcon": {"budget": 67500, "status": "active"},
    "Project Neptune": {"budget": 234000, "status": "paused"},
    "Project Zenith": {"budget": 15800, "status": "active"},
    "Project Cascade": {"budget": 450000, "status": "review"},
    "Project Ember": {"budget": 92100, "status": "active"},
}

# Test 1: memory.json exists and is under 2KB
memory_path = os.path.join(SETUP_DIR, "memory.json")
if os.path.exists(memory_path):
    memory_size = os.path.getsize(memory_path)
    if memory_size <= 2048:
        print(json.dumps({"test": "memory_file_size", "passed": True, "message": f"memory.json exists and is {memory_size} bytes (under 2KB limit)"}))
    else:
        print(json.dumps({"test": "memory_file_size", "passed": False, "message": f"memory.json is {memory_size} bytes, exceeds 2KB limit (2048 bytes)"}))
else:
    print(json.dumps({"test": "memory_file_size", "passed": False, "message": "memory.json does not exist"}))

# Test 2: answers.json exists
answers_path = os.path.join(SETUP_DIR, "answers.json")
if os.path.exists(answers_path):
    print(json.dumps({"test": "answers_file_exists", "passed": True, "message": "answers.json exists"}))
else:
    print(json.dumps({"test": "answers_file_exists", "passed": False, "message": "answers.json does not exist"}))
    sys.exit(0)

# Load answers
try:
    with open(answers_path, "r") as f:
        answers = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answers_valid_json", "passed": False, "message": f"answers.json is not valid JSON: {e}"}))
    sys.exit(0)

projects = answers.get("important_projects", [])
project_map = {}
for p in projects:
    name = p.get("name", "")
    project_map[name] = p

# Test 3: All 5 important project names present
found_names = set(project_map.keys())
expected_names = set(EXPECTED_PROJECTS.keys())
missing = expected_names - found_names
if not missing:
    print(json.dumps({"test": "all_important_names", "passed": True, "message": "All 5 important project names found in answers"}))
else:
    print(json.dumps({"test": "all_important_names", "passed": False, "message": f"Missing important projects: {', '.join(sorted(missing))}"}))

# Test 4: Correct budgets for each important project
budget_errors = []
for name, expected in EXPECTED_PROJECTS.items():
    if name in project_map:
        actual_budget = project_map[name].get("budget")
        if actual_budget is not None:
            try:
                actual_budget = int(actual_budget)
            except (ValueError, TypeError):
                try:
                    actual_budget = int(float(actual_budget))
                except (ValueError, TypeError):
                    budget_errors.append(f"{name}: budget '{actual_budget}' is not a valid number")
                    continue
            if actual_budget != expected["budget"]:
                budget_errors.append(f"{name}: expected ${expected['budget']:,}, got ${actual_budget:,}")
        else:
            budget_errors.append(f"{name}: budget field missing")

if not budget_errors:
    print(json.dumps({"test": "correct_budgets", "passed": True, "message": "All important projects have correct budgets"}))
else:
    print(json.dumps({"test": "correct_budgets", "passed": False, "message": "; ".join(budget_errors)}))

# Test 5: No non-important projects included
extra = found_names - expected_names
if not extra:
    print(json.dumps({"test": "no_extra_projects", "passed": True, "message": "No non-important projects included in answers"}))
else:
    print(json.dumps({"test": "no_extra_projects", "passed": False, "message": f"Non-important projects included: {', '.join(sorted(extra))}"}))
