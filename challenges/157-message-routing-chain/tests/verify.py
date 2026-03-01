#!/usr/bin/env python3
"""Verification script for Challenge 157: Message Routing Chain"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
MESSAGES_DIR = os.path.join(SETUP_DIR, "messages")


def main():
    # Test 1: msg_001.json exists and has correct structure
    msg1_path = os.path.join(MESSAGES_DIR, "msg_001.json")
    if not os.path.exists(msg1_path):
        print(json.dumps({"test": "msg_001_exists", "passed": False, "message": "setup/messages/msg_001.json does not exist"}))
    else:
        try:
            with open(msg1_path, "r") as f:
                msg1 = json.load(f)
            has_fields = (
                msg1.get("from") == "source"
                and msg1.get("to") == "processor"
                and msg1.get("payload") == "hello world"
            )
            if has_fields:
                print(json.dumps({"test": "msg_001_correct", "passed": True, "message": "msg_001.json has correct source message"}))
            else:
                print(json.dumps({"test": "msg_001_correct", "passed": False, "message": f"msg_001.json has incorrect content: {msg1}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "msg_001_valid", "passed": False, "message": f"Could not parse msg_001.json: {e}"}))

    # Test 2: msg_002.json exists and has correct structure
    msg2_path = os.path.join(MESSAGES_DIR, "msg_002.json")
    if not os.path.exists(msg2_path):
        print(json.dumps({"test": "msg_002_exists", "passed": False, "message": "setup/messages/msg_002.json does not exist"}))
    else:
        try:
            with open(msg2_path, "r") as f:
                msg2 = json.load(f)
            has_fields = (
                msg2.get("from") == "processor"
                and msg2.get("to") == "sink"
                and msg2.get("payload") == "HELLO WORLD"
            )
            if has_fields:
                print(json.dumps({"test": "msg_002_correct", "passed": True, "message": "msg_002.json has correct processed message with uppercase payload"}))
            else:
                print(json.dumps({"test": "msg_002_correct", "passed": False, "message": f"msg_002.json has incorrect content: {msg2}"}))
        except (json.JSONDecodeError, IOError) as e:
            print(json.dumps({"test": "msg_002_valid", "passed": False, "message": f"Could not parse msg_002.json: {e}"}))

    # Test 3: Payload was transformed to uppercase
    msg2_exists = os.path.exists(msg2_path)
    if msg2_exists:
        try:
            with open(msg2_path, "r") as f:
                msg2 = json.load(f)
            payload = msg2.get("payload", "")
            if payload == payload.upper() and payload == "HELLO WORLD":
                print(json.dumps({"test": "payload_uppercase", "passed": True, "message": "Payload correctly transformed to uppercase"}))
            else:
                print(json.dumps({"test": "payload_uppercase", "passed": False, "message": f"Expected uppercase payload 'HELLO WORLD', got '{payload}'"}))
        except (json.JSONDecodeError, IOError):
            print(json.dumps({"test": "payload_uppercase", "passed": False, "message": "Could not verify payload transformation"}))
    else:
        print(json.dumps({"test": "payload_uppercase", "passed": False, "message": "msg_002.json missing, cannot verify transformation"}))

    # Test 4: Routing chain is source -> processor -> sink
    chain_correct = False
    if os.path.exists(msg1_path) and os.path.exists(msg2_path):
        try:
            with open(msg1_path, "r") as f:
                m1 = json.load(f)
            with open(msg2_path, "r") as f:
                m2 = json.load(f)
            chain_correct = (
                m1.get("from") == "source"
                and m1.get("to") == "processor"
                and m2.get("from") == "processor"
                and m2.get("to") == "sink"
            )
        except (json.JSONDecodeError, IOError):
            pass

    if chain_correct:
        print(json.dumps({"test": "routing_chain", "passed": True, "message": "Routing chain is correct: source -> processor -> sink"}))
    else:
        print(json.dumps({"test": "routing_chain", "passed": False, "message": "Routing chain is incorrect or incomplete"}))

    # Test 5: answer.txt exists and equals "HELLO WORLD"
    answer_path = os.path.join(SETUP_DIR, "answer.txt")
    if not os.path.exists(answer_path):
        print(json.dumps({"test": "answer_exists", "passed": False, "message": "setup/answer.txt does not exist"}))
    else:
        with open(answer_path, "r") as f:
            answer = f.read().strip()
        if answer == "HELLO WORLD":
            print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains 'HELLO WORLD'"}))
        else:
            print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'HELLO WORLD' in answer.txt, got '{answer}'"}))


if __name__ == "__main__":
    main()
