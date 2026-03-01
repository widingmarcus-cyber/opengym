#!/usr/bin/env python3
"""Verification script for Challenge 144: Memory Schema Migration"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: data.json exists and is valid JSON
    data_path = os.path.join(SETUP_DIR, "data.json")
    if not os.path.exists(data_path):
        print(json.dumps({"test": "data_exists", "passed": False, "message": "setup/data.json does not exist"}))
        sys.exit(0)

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "data_exists", "passed": False, "message": f"Could not parse data.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "data_exists", "passed": True, "message": "data.json exists and is valid JSON"}))

    # Test 2: data.json has exactly 2 records
    if not isinstance(data, list):
        print(json.dumps({"test": "record_count", "passed": False, "message": f"Expected data to be an array, got {type(data).__name__}"}))
        sys.exit(0)

    if len(data) == 2:
        print(json.dumps({"test": "record_count", "passed": True, "message": "data.json has exactly 2 records"}))
    else:
        print(json.dumps({"test": "record_count", "passed": False, "message": f"Expected 2 records, got {len(data)}"}))

    # Test 3: All records have "full_name" field
    all_have_full_name = all(isinstance(r, dict) and "full_name" in r for r in data)
    if all_have_full_name:
        print(json.dumps({"test": "has_full_name", "passed": True, "message": "All records have 'full_name' field"}))
    else:
        print(json.dumps({"test": "has_full_name", "passed": False, "message": "Not all records have 'full_name' field"}))

    # Test 4: All records have "age" field
    all_have_age = all(isinstance(r, dict) and "age" in r for r in data)
    if all_have_age:
        print(json.dumps({"test": "has_age", "passed": True, "message": "All records have 'age' field"}))
    else:
        print(json.dumps({"test": "has_age", "passed": False, "message": "Not all records have 'age' field"}))

    # Test 5: All records have "active" field set to True
    all_have_active = all(isinstance(r, dict) and r.get("active") is True for r in data)
    if all_have_active:
        print(json.dumps({"test": "has_active", "passed": True, "message": "All records have 'active' field set to true"}))
    else:
        print(json.dumps({"test": "has_active", "passed": False, "message": "Not all records have 'active' set to true"}))

    # Test 6: No records have old "name" field
    none_have_name = all(isinstance(r, dict) and "name" not in r for r in data)
    if none_have_name:
        print(json.dumps({"test": "no_old_name_field", "passed": True, "message": "No records have the old 'name' field"}))
    else:
        print(json.dumps({"test": "no_old_name_field", "passed": False, "message": "Some records still have the old 'name' field"}))

    # Test 7: Correct values preserved (Alice=30, Bob=25)
    names = sorted([r.get("full_name", "") for r in data if isinstance(r, dict)])
    ages = {r.get("full_name"): r.get("age") for r in data if isinstance(r, dict)}
    if names == ["Alice", "Bob"] and ages.get("Alice") == 30 and ages.get("Bob") == 25:
        print(json.dumps({"test": "values_preserved", "passed": True, "message": "Original values preserved correctly (Alice=30, Bob=25)"}))
    else:
        print(json.dumps({"test": "values_preserved", "passed": False, "message": f"Values not preserved correctly: names={names}, ages={ages}"}))

    # Test 8: answer.txt exists and contains "2"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        sys.exit(0)

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "2":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '2'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '2' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
