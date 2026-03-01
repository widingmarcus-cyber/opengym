#!/usr/bin/env python3
"""Verification script for Challenge 145: Memory Integrity Checksum"""
import hashlib
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: data.json exists and is valid JSON
    data_path = os.path.join(SETUP_DIR, "data.json")
    if not os.path.exists(data_path):
        print(json.dumps({"test": "data_exists", "passed": False, "message": "setup/data.json does not exist"}))
        sys.exit(0)

    try:
        with open(data_path, "r") as f:
            data_content = f.read()
        data = json.loads(data_content)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "data_exists", "passed": False, "message": f"Could not parse data.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "data_exists", "passed": True, "message": "data.json exists and is valid JSON"}))

    # Test 2: data.json has the expected structure
    records = data.get("records", [])
    if isinstance(records, list) and len(records) == 3:
        ids = [r.get("id") for r in records if isinstance(r, dict)]
        values = [r.get("value") for r in records if isinstance(r, dict)]
        if ids == [1, 2, 3] and values == ["alpha", "beta", "gamma"]:
            print(json.dumps({"test": "data_content_correct", "passed": True, "message": "data.json has correct records"}))
        else:
            print(json.dumps({"test": "data_content_correct", "passed": False, "message": f"Unexpected record content: ids={ids}, values={values}"}))
    else:
        print(json.dumps({"test": "data_content_correct", "passed": False, "message": f"Expected 3 records, got {len(records) if isinstance(records, list) else 'not a list'}"}))

    # Test 3: checksum.txt exists
    checksum_path = os.path.join(SETUP_DIR, "checksum.txt")
    if not os.path.exists(checksum_path):
        print(json.dumps({"test": "checksum_exists", "passed": False, "message": "setup/checksum.txt does not exist"}))
        sys.exit(0)

    with open(checksum_path, "r") as f:
        stored_checksum = f.read().strip()

    print(json.dumps({"test": "checksum_exists", "passed": True, "message": "checksum.txt exists"}))

    # Test 4: checksum.txt matches the actual SHA-256 of data.json
    with open(data_path, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    if stored_checksum == actual_hash:
        print(json.dumps({"test": "checksum_correct", "passed": True, "message": "checksum.txt matches SHA-256 of data.json"}))
    else:
        print(json.dumps({"test": "checksum_correct", "passed": False, "message": f"Checksum mismatch: stored={stored_checksum}, actual={actual_hash}"}))

    # Test 5: status.txt exists and contains "VALID"
    status_path = os.path.join(SETUP_DIR, "status.txt")
    if not os.path.exists(status_path):
        print(json.dumps({"test": "status_exists", "passed": False, "message": "setup/status.txt does not exist"}))
        sys.exit(0)

    with open(status_path, "r") as f:
        status = f.read().strip()

    if status == "VALID":
        print(json.dumps({"test": "status_correct", "passed": True, "message": "status.txt contains 'VALID'"}))
    else:
        print(json.dumps({"test": "status_correct", "passed": False, "message": f"Expected 'VALID' in status.txt, got '{status}'"}))


if __name__ == "__main__":
    main()
