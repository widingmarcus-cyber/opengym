#!/usr/bin/env python3
"""Verification script for Challenge 158: Out-of-Order Event Handling"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: ordered.json exists and is valid JSON
    ordered_path = os.path.join(SETUP_DIR, "ordered.json")
    if not os.path.exists(ordered_path):
        print(json.dumps({"test": "ordered_exists", "passed": False, "message": "setup/ordered.json does not exist"}))
        sys.exit(0)

    try:
        with open(ordered_path, "r") as f:
            ordered = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "ordered_valid", "passed": False, "message": f"Could not parse ordered.json: {e}"}))
        sys.exit(0)

    if not isinstance(ordered, list):
        print(json.dumps({"test": "ordered_is_array", "passed": False, "message": "ordered.json must be a JSON array"}))
        sys.exit(0)

    print(json.dumps({"test": "ordered_exists", "passed": True, "message": "ordered.json exists and is valid JSON array"}))

    # Test 2: ordered.json has 5 entries
    if len(ordered) == 5:
        print(json.dumps({"test": "ordered_count", "passed": True, "message": "ordered.json has 5 entries"}))
    else:
        print(json.dumps({"test": "ordered_count", "passed": False, "message": f"Expected 5 entries, got {len(ordered)}"}))

    # Test 3: Events are sorted by seq 1-5
    expected_seqs = [1, 2, 3, 4, 5]
    actual_seqs = [e.get("seq") for e in ordered]
    if actual_seqs == expected_seqs:
        print(json.dumps({"test": "ordered_by_seq", "passed": True, "message": "Events are sorted by seq 1, 2, 3, 4, 5"}))
    else:
        print(json.dumps({"test": "ordered_by_seq", "passed": False, "message": f"Expected seq order {expected_seqs}, got {actual_seqs}"}))

    # Test 4: Data values match expected order
    expected_data = ["alpha", "beta", "gamma", "delta", "epsilon"]
    actual_data = [e.get("data") for e in ordered]
    if actual_data == expected_data:
        print(json.dumps({"test": "ordered_data_correct", "passed": True, "message": "Data values are in correct order"}))
    else:
        print(json.dumps({"test": "ordered_data_correct", "passed": False, "message": f"Expected data {expected_data}, got {actual_data}"}))

    # Test 5: answer.txt exists and is correct
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        return

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    expected_answer = "alpha,beta,gamma,delta,epsilon"
    if answer == expected_answer:
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains 'alpha,beta,gamma,delta,epsilon'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '{expected_answer}', got '{answer}'"}))


if __name__ == "__main__":
    main()
