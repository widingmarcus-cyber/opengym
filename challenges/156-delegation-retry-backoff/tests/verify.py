#!/usr/bin/env python3
"""Verification script for Challenge 156: Delegation Retry with Backoff"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: result.txt exists and equals "SUCCESS"
    result_path = os.path.join(SETUP_DIR, "result.txt")
    if not os.path.exists(result_path):
        print(json.dumps({"test": "result_exists", "passed": False, "message": "setup/result.txt does not exist"}))
    else:
        with open(result_path, "r") as f:
            result = f.read().strip()
        if result == "SUCCESS":
            print(json.dumps({"test": "result_success", "passed": True, "message": "result.txt contains 'SUCCESS'"}))
        else:
            print(json.dumps({"test": "result_success", "passed": False, "message": f"Expected 'SUCCESS' in result.txt, got '{result}'"}))

    # Test 2: retry_log.json exists and is valid JSON array
    log_path = os.path.join(SETUP_DIR, "retry_log.json")
    if not os.path.exists(log_path):
        print(json.dumps({"test": "retry_log_exists", "passed": False, "message": "setup/retry_log.json does not exist"}))
        sys.exit(0)

    try:
        with open(log_path, "r") as f:
            log = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "retry_log_valid", "passed": False, "message": f"Could not parse retry_log.json: {e}"}))
        sys.exit(0)

    if not isinstance(log, list):
        print(json.dumps({"test": "retry_log_is_array", "passed": False, "message": "retry_log.json must be a JSON array"}))
        sys.exit(0)

    print(json.dumps({"test": "retry_log_exists", "passed": True, "message": "retry_log.json exists and is valid JSON array"}))

    # Test 3: retry_log has 3 entries
    if len(log) == 3:
        print(json.dumps({"test": "retry_log_count", "passed": True, "message": "retry_log.json has 3 entries"}))
    else:
        print(json.dumps({"test": "retry_log_count", "passed": False, "message": f"Expected 3 entries in retry_log.json, got {len(log)}"}))

    # Test 4: First two attempts failed, third succeeded
    statuses_correct = True
    if len(log) >= 3:
        if log[0].get("status") != "failed":
            statuses_correct = False
        if log[1].get("status") != "failed":
            statuses_correct = False
        if log[2].get("status") != "success":
            statuses_correct = False
    else:
        statuses_correct = False

    if statuses_correct:
        print(json.dumps({"test": "retry_statuses", "passed": True, "message": "Attempts 1-2 failed, attempt 3 succeeded"}))
    else:
        print(json.dumps({"test": "retry_statuses", "passed": False, "message": "Expected failed, failed, success pattern in retry log"}))

    # Test 5: Backoff shows increasing wait times (exponential pattern)
    backoff_correct = False
    if len(log) >= 3:
        w1 = log[0].get("wait_seconds", -1)
        w2 = log[1].get("wait_seconds", -1)
        w3 = log[2].get("wait_seconds", -1)
        # Exponential: w2 > w1 > 0, and last attempt has wait 0
        if w1 > 0 and w2 > w1 and w3 == 0:
            backoff_correct = True

    if backoff_correct:
        print(json.dumps({"test": "backoff_pattern", "passed": True, "message": "Backoff shows increasing wait times with exponential pattern"}))
    else:
        print(json.dumps({"test": "backoff_pattern", "passed": False, "message": "Expected exponential backoff: increasing waits for failures, 0 for success"}))

    # Test 6: answer.json exists and is correct
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

    if answer.get("total_attempts") == 3:
        print(json.dumps({"test": "answer_total_attempts", "passed": True, "message": "answer.json total_attempts is 3"}))
    else:
        print(json.dumps({"test": "answer_total_attempts", "passed": False, "message": f"Expected total_attempts 3, got {answer.get('total_attempts')}"}))

    if answer.get("backoff_pattern") == "exponential":
        print(json.dumps({"test": "answer_backoff_pattern", "passed": True, "message": "answer.json backoff_pattern is 'exponential'"}))
    else:
        print(json.dumps({"test": "answer_backoff_pattern", "passed": False, "message": f"Expected backoff_pattern 'exponential', got '{answer.get('backoff_pattern')}'"}))


if __name__ == "__main__":
    main()
