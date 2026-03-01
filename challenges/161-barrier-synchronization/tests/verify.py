#!/usr/bin/env python3
"""Verification script for Challenge 161: Barrier Synchronization"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Compute expected values from input data files
    expected_a = None
    expected_b = None
    data_a_path = os.path.join(SETUP_DIR, "data", "worker_a_input.json")
    data_b_path = os.path.join(SETUP_DIR, "data", "worker_b_input.json")
    try:
        with open(data_a_path, "r") as f:
            expected_a = sum(json.load(f)["values"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        expected_a = 42  # fallback
    try:
        with open(data_b_path, "r") as f:
            expected_b = sum(json.load(f)["values"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        expected_b = 58  # fallback
    expected_total = expected_a + expected_b

    # Test 1: barrier.json exists and shows both workers ready
    barrier_path = os.path.join(SETUP_DIR, "barrier.json")
    if not os.path.exists(barrier_path):
        print(json.dumps({"test": "barrier_exists", "passed": False, "message": "setup/barrier.json does not exist"}))
    else:
        try:
            with open(barrier_path, "r") as f:
                barrier = json.load(f)
            a_ready = barrier.get("worker_a") is True
            b_ready = barrier.get("worker_b") is True
            if a_ready and b_ready:
                print(json.dumps({"test": "barrier_both_ready", "passed": True, "message": "Both workers signaled ready at barrier"}))
            else:
                print(json.dumps({"test": "barrier_both_ready", "passed": False, "message": f"Expected both workers ready. worker_a={barrier.get('worker_a')}, worker_b={barrier.get('worker_b')}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "barrier_valid", "passed": False, "message": f"Could not parse barrier.json: {e}"}))

    # Test 2: worker_a.json exists with correct result
    worker_a_path = os.path.join(SETUP_DIR, "results", "worker_a.json")
    if not os.path.exists(worker_a_path):
        print(json.dumps({"test": "worker_a_exists", "passed": False, "message": "setup/results/worker_a.json does not exist"}))
    else:
        try:
            with open(worker_a_path, "r") as f:
                wa = json.load(f)
            if wa.get("done") is True and wa.get("result") == expected_a:
                print(json.dumps({"test": "worker_a_correct", "passed": True, "message": f"worker_a.json has done=true, result={expected_a}"}))
            else:
                print(json.dumps({"test": "worker_a_correct", "passed": False, "message": f"Expected done=true, result={expected_a}. Got {wa}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "worker_a_valid", "passed": False, "message": f"Could not parse worker_a.json: {e}"}))

    # Test 3: worker_b.json exists with correct result
    worker_b_path = os.path.join(SETUP_DIR, "results", "worker_b.json")
    if not os.path.exists(worker_b_path):
        print(json.dumps({"test": "worker_b_exists", "passed": False, "message": "setup/results/worker_b.json does not exist"}))
    else:
        try:
            with open(worker_b_path, "r") as f:
                wb = json.load(f)
            if wb.get("done") is True and wb.get("result") == expected_b:
                print(json.dumps({"test": "worker_b_correct", "passed": True, "message": f"worker_b.json has done=true, result={expected_b}"}))
            else:
                print(json.dumps({"test": "worker_b_correct", "passed": False, "message": f"Expected done=true, result={expected_b}. Got {wb}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "worker_b_valid", "passed": False, "message": f"Could not parse worker_b.json: {e}"}))

    # Test 4: answer.json exists and has correct values
    answer_path = os.path.join(SETUP_DIR, "answer.json")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.json does not exist"}))
        return

    try:
        with open(answer_path, "r") as f:
            answer = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "answer_valid", "passed": False, "message": f"Could not parse answer.json: {e}"}))
        return

    if answer.get("total") == expected_total:
        print(json.dumps({"test": "answer_total", "passed": True, "message": f"answer.json total is {expected_total}"}))
    else:
        print(json.dumps({"test": "answer_total", "passed": False, "message": f"Expected total {expected_total}, got {answer.get('total')}"}))

    if answer.get("all_ready") is True:
        print(json.dumps({"test": "answer_all_ready", "passed": True, "message": "answer.json all_ready is true"}))
    else:
        print(json.dumps({"test": "answer_all_ready", "passed": False, "message": f"Expected all_ready true, got {answer.get('all_ready')}"}))


if __name__ == "__main__":
    main()
