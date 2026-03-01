#!/usr/bin/env python3
"""Verification script for Challenge 163: Multi-Agent File Append Ordering"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: log.txt exists
    log_path = os.path.join(SETUP_DIR, "log.txt")
    if not os.path.exists(log_path):
        print(json.dumps({"test": "log_exists", "passed": False, "message": "setup/log.txt does not exist"}))
        sys.exit(0)

    with open(log_path, "r") as f:
        content = f.read()

    lines = [line for line in content.strip().split("\n") if line.strip()]

    print(json.dumps({"test": "log_exists", "passed": True, "message": "setup/log.txt exists"}))

    # Test 2: log.txt has exactly 3 lines
    if len(lines) == 3:
        print(json.dumps({"test": "log_line_count", "passed": True, "message": "log.txt has 3 lines"}))
    else:
        print(json.dumps({"test": "log_line_count", "passed": False, "message": f"Expected 3 lines, got {len(lines)}"}))

    # Test 3: First line is "A:step1"
    if len(lines) >= 1 and lines[0].strip() == "A:step1":
        print(json.dumps({"test": "line_1_correct", "passed": True, "message": "Line 1 is 'A:step1'"}))
    else:
        actual = lines[0].strip() if len(lines) >= 1 else "(missing)"
        print(json.dumps({"test": "line_1_correct", "passed": False, "message": f"Expected line 1 'A:step1', got '{actual}'"}))

    # Test 4: Second line is "B:step2"
    if len(lines) >= 2 and lines[1].strip() == "B:step2":
        print(json.dumps({"test": "line_2_correct", "passed": True, "message": "Line 2 is 'B:step2'"}))
    else:
        actual = lines[1].strip() if len(lines) >= 2 else "(missing)"
        print(json.dumps({"test": "line_2_correct", "passed": False, "message": f"Expected line 2 'B:step2', got '{actual}'"}))

    # Test 5: Third line is "C:step3"
    if len(lines) >= 3 and lines[2].strip() == "C:step3":
        print(json.dumps({"test": "line_3_correct", "passed": True, "message": "Line 3 is 'C:step3'"}))
    else:
        actual = lines[2].strip() if len(lines) >= 3 else "(missing)"
        print(json.dumps({"test": "line_3_correct", "passed": False, "message": f"Expected line 3 'C:step3', got '{actual}'"}))

    # Test 6: answer.txt exists and equals "3"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        return

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "3":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '3'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '3' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
