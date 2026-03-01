#!/usr/bin/env python3
"""Verification script for Challenge 164: Non-deterministic Ordering Exposure"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: results.json exists and is valid JSON
    results_path = os.path.join(SETUP_DIR, "results.json")
    if not os.path.exists(results_path):
        print(json.dumps({"test": "results_exists", "passed": False, "message": "setup/results.json does not exist"}))
        sys.exit(0)

    try:
        with open(results_path, "r") as f:
            results = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "results_valid", "passed": False, "message": f"Could not parse results.json: {e}"}))
        sys.exit(0)

    if not isinstance(results, list):
        print(json.dumps({"test": "results_is_array", "passed": False, "message": "results.json must be a JSON array"}))
        sys.exit(0)

    print(json.dumps({"test": "results_exists", "passed": True, "message": "results.json exists and is valid JSON array"}))

    # Test 2: results.json has 6 entries
    if len(results) == 6:
        print(json.dumps({"test": "results_count", "passed": True, "message": "results.json has 6 entries"}))
    else:
        print(json.dumps({"test": "results_count", "passed": False, "message": f"Expected 6 entries, got {len(results)}"}))

    # Test 3: Results are sorted by id (1, 2, 3, 4, 5, 6)
    ids = [r.get("id") for r in results]
    expected_ids = [1, 2, 3, 4, 5, 6]
    if ids == expected_ids:
        print(json.dumps({"test": "results_sorted", "passed": True, "message": "Results are sorted by id: 1, 2, 3, 4, 5, 6"}))
    else:
        print(json.dumps({"test": "results_sorted", "passed": False, "message": f"Expected ids {expected_ids}, got {ids}"}))

    # Test 4: All entries have "processed": true
    all_processed = all(r.get("processed") is True for r in results)
    if all_processed:
        print(json.dumps({"test": "all_processed", "passed": True, "message": "All entries have processed=true"}))
    else:
        print(json.dumps({"test": "all_processed", "passed": False, "message": "Not all entries have processed=true"}))

    # Test 5: Data values match expected
    expected_data = {1: "alpha", 2: "beta", 3: "gamma", 4: "delta", 5: "epsilon", 6: "zeta"}
    data_correct = True
    for r in results:
        rid = r.get("id")
        rdata = r.get("data")
        if expected_data.get(rid) != rdata:
            data_correct = False
            break

    if data_correct:
        print(json.dumps({"test": "data_correct", "passed": True, "message": "All data values match expected values"}))
    else:
        print(json.dumps({"test": "data_correct", "passed": False, "message": "Some data values do not match expected values"}))

    # Test 6: answer.txt exists and equals "SORTED"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        return

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "SORTED":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains 'SORTED'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'SORTED' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
