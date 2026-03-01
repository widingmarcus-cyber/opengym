#!/usr/bin/env python3
"""Verification script for Challenge 160: Lost Acknowledgement Recovery"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: outbox.json exists and is valid
    outbox_path = os.path.join(SETUP_DIR, "outbox.json")
    if not os.path.exists(outbox_path):
        print(json.dumps({"test": "outbox_exists", "passed": False, "message": "setup/outbox.json does not exist"}))
        sys.exit(0)

    try:
        with open(outbox_path, "r") as f:
            outbox = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "outbox_valid", "passed": False, "message": f"Could not parse outbox.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "outbox_exists", "passed": True, "message": "outbox.json exists and is valid JSON"}))

    # Test 2: outbox.json has m1 and m3 acked, m2 not acked
    outbox_map = {msg.get("id"): msg for msg in outbox}
    m1_acked = outbox_map.get("m1", {}).get("acked") is True
    m2_not_acked = outbox_map.get("m2", {}).get("acked") is False
    m3_acked = outbox_map.get("m3", {}).get("acked") is True

    if m1_acked and m3_acked:
        print(json.dumps({"test": "outbox_m1_m3_acked", "passed": True, "message": "m1 and m3 are marked as acked in outbox"}))
    else:
        print(json.dumps({"test": "outbox_m1_m3_acked", "passed": False, "message": f"Expected m1 and m3 acked=true. m1 acked={outbox_map.get('m1', {}).get('acked')}, m3 acked={outbox_map.get('m3', {}).get('acked')}"}))

    if m2_not_acked:
        print(json.dumps({"test": "outbox_m2_unacked", "passed": True, "message": "m2 remains unacked in outbox"}))
    else:
        print(json.dumps({"test": "outbox_m2_unacked", "passed": False, "message": f"Expected m2 acked=false, got acked={outbox_map.get('m2', {}).get('acked')}"}))

    # Test 3: inbox.json exists
    inbox_path = os.path.join(SETUP_DIR, "inbox.json")
    if os.path.exists(inbox_path):
        print(json.dumps({"test": "inbox_exists", "passed": True, "message": "inbox.json exists"}))
    else:
        print(json.dumps({"test": "inbox_exists", "passed": False, "message": "setup/inbox.json does not exist"}))

    # Test 4: answer.json exists and is correct
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

    # Check unacked
    unacked = answer.get("unacked")
    if isinstance(unacked, list) and unacked == ["m2"]:
        print(json.dumps({"test": "answer_unacked", "passed": True, "message": "answer.json unacked is ['m2']"}))
    else:
        print(json.dumps({"test": "answer_unacked", "passed": False, "message": f"Expected unacked ['m2'], got {unacked}"}))

    # Check total_sent
    if answer.get("total_sent") == 3:
        print(json.dumps({"test": "answer_total_sent", "passed": True, "message": "answer.json total_sent is 3"}))
    else:
        print(json.dumps({"test": "answer_total_sent", "passed": False, "message": f"Expected total_sent 3, got {answer.get('total_sent')}"}))

    # Check total_acked
    if answer.get("total_acked") == 2:
        print(json.dumps({"test": "answer_total_acked", "passed": True, "message": "answer.json total_acked is 2"}))
    else:
        print(json.dumps({"test": "answer_total_acked", "passed": False, "message": f"Expected total_acked 2, got {answer.get('total_acked')}"}))


if __name__ == "__main__":
    main()
