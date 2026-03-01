#!/usr/bin/env python3
"""Verification script for Challenge 142: Memory Rollback"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: answer.txt exists and contains "70"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
        sys.exit(0)

    with open(answer_path, "r") as f:
        answer = f.read().strip()

    if answer == "70":
        print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains '70'"}))
    else:
        print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '70' in answer.txt, got '{answer}'"}))

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

    # Test 3: state.json has balance = 70
    balance = state.get("balance")
    if balance == 70:
        print(json.dumps({"test": "balance_correct", "passed": True, "message": "state.json balance is 70"}))
    else:
        print(json.dumps({"test": "balance_correct", "passed": False, "message": f"Expected balance = 70, got {balance}"}))

    # Test 4: state.json has exactly 1 transaction
    transactions = state.get("transactions", [])
    if isinstance(transactions, list) and len(transactions) == 1:
        print(json.dumps({"test": "transaction_count", "passed": True, "message": "state.json has exactly 1 transaction"}))
    else:
        count = len(transactions) if isinstance(transactions, list) else "not a list"
        print(json.dumps({"test": "transaction_count", "passed": False, "message": f"Expected 1 transaction, got {count}"}))

    # Test 5: The single transaction is a withdrawal of 30
    if isinstance(transactions, list) and len(transactions) >= 1:
        tx = transactions[0]
        if isinstance(tx, dict) and tx.get("type") == "withdraw" and tx.get("amount") == 30:
            print(json.dumps({"test": "transaction_correct", "passed": True, "message": "Transaction is withdraw of 30"}))
        else:
            print(json.dumps({"test": "transaction_correct", "passed": False, "message": f"Expected withdraw 30, got {tx}"}))
    else:
        print(json.dumps({"test": "transaction_correct", "passed": False, "message": "No transactions to verify"}))

    # Test 6: history.json exists and has versions 1 and 2
    history_path = os.path.join(SETUP_DIR, "history.json")
    if not os.path.exists(history_path):
        print(json.dumps({"test": "history_exists", "passed": False, "message": "setup/history.json does not exist"}))
        sys.exit(0)

    try:
        with open(history_path, "r") as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "history_exists", "passed": False, "message": f"Could not parse history.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "history_exists", "passed": True, "message": "history.json exists and is valid JSON"}))

    # Test 7: history has exactly 2 versions (1 and 2, no version 3)
    if not isinstance(history, list):
        print(json.dumps({"test": "history_versions", "passed": False, "message": f"Expected history to be an array, got {type(history).__name__}"}))
        sys.exit(0)

    versions = set()
    for entry in history:
        if isinstance(entry, dict) and "version" in entry:
            versions.add(entry["version"])

    if versions == {1, 2}:
        print(json.dumps({"test": "history_versions", "passed": True, "message": "history.json has exactly versions 1 and 2"}))
    else:
        print(json.dumps({"test": "history_versions", "passed": False, "message": f"Expected versions {{1, 2}}, got {sorted(versions)}"}))

    # Test 8: No failed transaction (version 3) in history
    if 3 in versions:
        print(json.dumps({"test": "no_failed_version", "passed": False, "message": "history.json contains version 3 (failed transaction was not rolled back)"}))
    else:
        print(json.dumps({"test": "no_failed_version", "passed": True, "message": "No version 3 in history (failed transaction correctly excluded)"}))


if __name__ == "__main__":
    main()
