#!/usr/bin/env python3
"""Verification script for Challenge 134: Indexed Retrieval Constraint"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
DATA_DIR = os.path.join(SETUP_DIR, "data")

# Test 1: index.json exists and is valid JSON
index_path = os.path.join(SETUP_DIR, "index.json")
if not os.path.exists(index_path):
    print(json.dumps({"test": "index_file_exists", "passed": False, "message": "index.json does not exist"}))
    sys.exit(0)

try:
    with open(index_path, "r") as f:
        index = json.load(f)
    print(json.dumps({"test": "index_file_exists", "passed": True, "message": "index.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "index_file_exists", "passed": False, "message": f"index.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: index.json maps categories to lists of filenames
if not isinstance(index, dict):
    print(json.dumps({"test": "index_structure", "passed": False, "message": "index.json is not a JSON object"}))
    sys.exit(0)

expected_categories = {"A", "B", "C"}
actual_categories = set(index.keys())
all_lists = all(isinstance(v, list) for v in index.values())

if actual_categories == expected_categories and all_lists:
    print(json.dumps({"test": "index_structure", "passed": True, "message": "index.json maps categories A, B, C to lists"}))
elif not all_lists:
    print(json.dumps({"test": "index_structure", "passed": False, "message": "Not all category values are lists"}))
else:
    print(json.dumps({"test": "index_structure", "passed": False, "message": f"Expected categories A, B, C; found {sorted(actual_categories)}"}))

# Test 3: index contains only filenames (not full records)
index_contains_only_filenames = True
bad_entries = []
for cat, filenames in index.items():
    if isinstance(filenames, list):
        for entry in filenames:
            if not isinstance(entry, str) or not entry.endswith(".json"):
                index_contains_only_filenames = False
                bad_entries.append(f"{cat}: {entry}")

if index_contains_only_filenames:
    print(json.dumps({"test": "index_filenames_only", "passed": True, "message": "Index contains only filename strings"}))
else:
    print(json.dumps({"test": "index_filenames_only", "passed": False, "message": f"Index contains non-filename entries: {bad_entries[:5]}"}))

# Test 4: Category B in index has the correct files
expected_b_files = sorted(["record_02.json", "record_07.json", "record_11.json", "record_16.json"])
actual_b_files = sorted(index.get("B", []))
if actual_b_files == expected_b_files:
    print(json.dumps({"test": "category_b_files", "passed": True, "message": "Category B index contains the correct 4 files"}))
else:
    print(json.dumps({"test": "category_b_files", "passed": False, "message": f"Expected {expected_b_files}, got {actual_b_files}"}))

# Test 5: answer.txt exists and contains "90"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "90":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains the correct sum '90'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '90' in answer.txt, got '{answer}'"}))

# Test 6: Data files were not modified (spot check)
spot_check_passed = True
spot_check_msg = ""
try:
    with open(os.path.join(DATA_DIR, "record_02.json"), "r") as f:
        r2 = json.load(f)
    if r2 != {"id": 2, "category": "B", "value": 15}:
        spot_check_passed = False
        spot_check_msg = f"record_02.json was modified: {r2}"
    with open(os.path.join(DATA_DIR, "record_16.json"), "r") as f:
        r16 = json.load(f)
    if r16 != {"id": 16, "category": "B", "value": 44}:
        spot_check_passed = False
        spot_check_msg = f"record_16.json was modified: {r16}"
except Exception as e:
    spot_check_passed = False
    spot_check_msg = f"Error reading data files: {e}"

if spot_check_passed:
    print(json.dumps({"test": "data_files_unmodified", "passed": True, "message": "Data files were not modified"}))
else:
    print(json.dumps({"test": "data_files_unmodified", "passed": False, "message": spot_check_msg}))
