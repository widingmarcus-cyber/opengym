#!/usr/bin/env python3
"""Verification script for Challenge 143: Memory Snapshot Restore"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: answer.txt exists and contains "light"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        sys.exit(0)

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "light":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains 'light'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'light' in answer.txt, got '{answer}'"}))

    # Test 2: state.json exists and is valid JSON
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

    # Test 3: state.json has users = ["alice"]
    users = state.get("users")
    if isinstance(users, list) and users == ["alice"]:
        print(json.dumps({"test": "state_users_correct", "passed": True, "message": "state.json users is ['alice']"}))
    else:
        print(json.dumps({"test": "state_users_correct", "passed": False, "message": f"Expected users ['alice'], got {users}"}))

    # Test 4: state.json has config.theme = "light"
    config = state.get("config", {})
    theme = config.get("theme") if isinstance(config, dict) else None
    if theme == "light":
        print(json.dumps({"test": "state_theme_correct", "passed": True, "message": "state.json config.theme is 'light'"}))
    else:
        print(json.dumps({"test": "state_theme_correct", "passed": False, "message": f"Expected config.theme 'light', got '{theme}'"}))

    # Test 5: snap_1.json exists
    snap1_path = os.path.join(SETUP_DIR, "snapshots", "snap_1.json")
    if os.path.exists(snap1_path):
        print(json.dumps({"test": "snap1_exists", "passed": True, "message": "setup/snapshots/snap_1.json exists"}))
    else:
        print(json.dumps({"test": "snap1_exists", "passed": False, "message": "setup/snapshots/snap_1.json does not exist"}))

    # Test 6: snap_2.json exists
    snap2_path = os.path.join(SETUP_DIR, "snapshots", "snap_2.json")
    if os.path.exists(snap2_path):
        print(json.dumps({"test": "snap2_exists", "passed": True, "message": "setup/snapshots/snap_2.json exists"}))
    else:
        print(json.dumps({"test": "snap2_exists", "passed": False, "message": "setup/snapshots/snap_2.json does not exist"}))

    # Test 7: snap_1.json has correct content (original state)
    if os.path.exists(snap1_path):
        try:
            with open(snap1_path, "r") as f:
                snap1 = json.load(f)
            snap1_users = snap1.get("users")
            snap1_theme = snap1.get("config", {}).get("theme") if isinstance(snap1.get("config"), dict) else None
            if snap1_users == ["alice"] and snap1_theme == "light":
                print(json.dumps({"test": "snap1_content_correct", "passed": True, "message": "snap_1.json has correct original state"}))
            else:
                print(json.dumps({"test": "snap1_content_correct", "passed": False, "message": f"snap_1.json content incorrect: users={snap1_users}, theme={snap1_theme}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "snap1_content_correct", "passed": False, "message": f"Could not parse snap_1.json: {e}"}))

    # Test 8: snap_2.json has modified content
    if os.path.exists(snap2_path):
        try:
            with open(snap2_path, "r") as f:
                snap2 = json.load(f)
            snap2_users = snap2.get("users")
            snap2_theme = snap2.get("config", {}).get("theme") if isinstance(snap2.get("config"), dict) else None
            if isinstance(snap2_users, list) and "bob" in snap2_users and snap2_theme == "dark":
                print(json.dumps({"test": "snap2_content_correct", "passed": True, "message": "snap_2.json has modified state with bob and dark theme"}))
            else:
                print(json.dumps({"test": "snap2_content_correct", "passed": False, "message": f"snap_2.json content incorrect: users={snap2_users}, theme={snap2_theme}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "snap2_content_correct", "passed": False, "message": f"Could not parse snap_2.json: {e}"}))


if __name__ == "__main__":
    main()
