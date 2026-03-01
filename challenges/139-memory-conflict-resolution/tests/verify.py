#!/usr/bin/env python3
"""Verification script for Challenge 139: Memory Conflict Resolution"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: state.json exists and is valid JSON
    state_path = os.path.join(SETUP_DIR, "state.json")
    if not os.path.exists(state_path):
        print(json.dumps({"test": "state_exists", "passed": False, "message": "setup/state.json does not exist"}))
        sys.exit(0)

    try:
        with open(state_path, "r") as f:
            state = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "state_exists", "passed": False, "message": f"Could not parse state.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "state_exists", "passed": True, "message": "state.json exists and is valid JSON"}))

    # Test 2: state.json has port = 9090
    port = None
    if isinstance(state, dict) and "config" in state and isinstance(state["config"], dict):
        port = state["config"].get("port")

    if port == 9090:
        print(json.dumps({"test": "port_is_9090", "passed": True, "message": "state.json config.port is 9090"}))
    else:
        print(json.dumps({"test": "port_is_9090", "passed": False, "message": f"Expected config.port = 9090, got {port}"}))

    # Test 3: state.json preserves host = localhost
    host = None
    if isinstance(state, dict) and "config" in state and isinstance(state["config"], dict):
        host = state["config"].get("host")

    if host == "localhost":
        print(json.dumps({"test": "host_preserved", "passed": True, "message": "state.json config.host is still 'localhost'"}))
    else:
        print(json.dumps({"test": "host_preserved", "passed": False, "message": f"Expected config.host = 'localhost', got '{host}'"}))

    # Test 4: policy.txt exists and contains "last-write-wins"
    policy_path = os.path.join(SETUP_DIR, "policy.txt")
    if not os.path.exists(policy_path):
        print(json.dumps({"test": "policy_correct", "passed": False, "message": "setup/policy.txt does not exist"}))
    else:
        with open(policy_path, "r") as f:
            policy = f.read().strip()
        if policy == "last-write-wins":
            print(json.dumps({"test": "policy_correct", "passed": True, "message": "policy.txt contains 'last-write-wins'"}))
        else:
            print(json.dumps({"test": "policy_correct", "passed": False, "message": f"Expected 'last-write-wins', got '{policy}'"}))

    # Test 5: answer.txt exists and contains "9090"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_correct", "passed": False, "message": "setup/answer.txt does not exist"}))
    else:
        with open(answer_path, "r") as f:
            answer = f.read().strip()
        if answer == "9090":
            print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '9090'"}))
        else:
            print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '9090' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
