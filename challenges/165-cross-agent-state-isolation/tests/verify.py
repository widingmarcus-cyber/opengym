#!/usr/bin/env python3
"""Verification script for Challenge 165: Cross-Agent State Isolation"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: shared_output.json exists and is valid
    shared_path = os.path.join(SETUP_DIR, "shared_output.json")
    if not os.path.exists(shared_path):
        print(json.dumps({"test": "shared_output_exists", "passed": False, "message": "setup/shared_output.json does not exist"}))
        sys.exit(0)

    try:
        with open(shared_path, "r") as f:
            shared_raw = f.read()
        shared = json.loads(shared_raw)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "shared_output_valid", "passed": False, "message": f"Could not parse shared_output.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "shared_output_exists", "passed": True, "message": "shared_output.json exists and is valid JSON"}))

    # Test 2: shared_output.json has agent_a_data
    a_data = shared.get("agent_a_data")
    if isinstance(a_data, list) and a_data == [1, 2, 3]:
        print(json.dumps({"test": "agent_a_data_correct", "passed": True, "message": "shared_output.json has agent_a_data = [1, 2, 3]"}))
    else:
        print(json.dumps({"test": "agent_a_data_correct", "passed": False, "message": f"Expected agent_a_data [1, 2, 3], got {a_data}"}))

    # Test 3: shared_output.json has agent_b_data
    b_data = shared.get("agent_b_data")
    if isinstance(b_data, list) and b_data == [4, 5, 6]:
        print(json.dumps({"test": "agent_b_data_correct", "passed": True, "message": "shared_output.json has agent_b_data = [4, 5, 6]"}))
    else:
        print(json.dumps({"test": "agent_b_data_correct", "passed": False, "message": f"Expected agent_b_data [4, 5, 6], got {b_data}"}))

    # Test 4: No secrets leaked into shared_output.json
    secrets = ["alpha_key", "beta_key"]
    leaked = [s for s in secrets if s in shared_raw]
    if not leaked:
        print(json.dumps({"test": "no_secrets_in_shared", "passed": True, "message": "No secrets leaked into shared_output.json"}))
    else:
        print(json.dumps({"test": "no_secrets_in_shared", "passed": False, "message": f"Secrets leaked into shared_output.json: {leaked}"}))

    # Test 5: agent_a_state.json has secret
    a_state_path = os.path.join(SETUP_DIR, "agent_a_state.json")
    if os.path.exists(a_state_path):
        try:
            with open(a_state_path, "r") as f:
                a_state = json.load(f)
            if a_state.get("secret") == "alpha_key":
                print(json.dumps({"test": "agent_a_has_secret", "passed": True, "message": "agent_a_state.json has secret 'alpha_key'"}))
            else:
                print(json.dumps({"test": "agent_a_has_secret", "passed": False, "message": f"Expected secret 'alpha_key', got '{a_state.get('secret')}'"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "agent_a_state_valid", "passed": False, "message": f"Could not parse agent_a_state.json: {e}"}))
    else:
        print(json.dumps({"test": "agent_a_has_secret", "passed": False, "message": "setup/agent_a_state.json does not exist"}))

    # Test 6: agent_b_state.json has secret
    b_state_path = os.path.join(SETUP_DIR, "agent_b_state.json")
    if os.path.exists(b_state_path):
        try:
            with open(b_state_path, "r") as f:
                b_state = json.load(f)
            if b_state.get("secret") == "beta_key":
                print(json.dumps({"test": "agent_b_has_secret", "passed": True, "message": "agent_b_state.json has secret 'beta_key'"}))
            else:
                print(json.dumps({"test": "agent_b_has_secret", "passed": False, "message": f"Expected secret 'beta_key', got '{b_state.get('secret')}'"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "agent_b_state_valid", "passed": False, "message": f"Could not parse agent_b_state.json: {e}"}))
    else:
        print(json.dumps({"test": "agent_b_has_secret", "passed": False, "message": "setup/agent_b_state.json does not exist"}))

    # Test 7: answer.json exists and is correct
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

    if answer.get("total_items") == 6:
        print(json.dumps({"test": "answer_total_items", "passed": True, "message": "answer.json total_items is 6"}))
    else:
        print(json.dumps({"test": "answer_total_items", "passed": False, "message": f"Expected total_items 6, got {answer.get('total_items')}"}))

    if answer.get("secrets_leaked") is False:
        print(json.dumps({"test": "answer_secrets_leaked", "passed": True, "message": "answer.json secrets_leaked is false"}))
    else:
        print(json.dumps({"test": "answer_secrets_leaked", "passed": False, "message": f"Expected secrets_leaked false, got {answer.get('secrets_leaked')}"}))


if __name__ == "__main__":
    main()
