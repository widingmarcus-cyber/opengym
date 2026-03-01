#!/usr/bin/env python3
"""Verification script for Challenge 140: Memory Corruption Detection"""
import hashlib
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")


def main():
    # Test 1: status.txt exists and contains "RESTORED"
    status_path = os.path.join(SETUP_DIR, "status.txt")
    if not os.path.exists(status_path):
        print(json.dumps({"test": "status_exists", "passed": False, "message": "setup/status.txt does not exist"}))
        sys.exit(0)

    with open(status_path, "r") as f:
        status = f.read().strip()

    if status == "RESTORED":
        print(json.dumps({"test": "status_restored", "passed": True, "message": "status.txt contains 'RESTORED'"}))
    else:
        print(json.dumps({"test": "status_restored", "passed": False, "message": f"Expected 'RESTORED' in status.txt, got '{status}'"}))

    # Test 2: data.json exists and is valid JSON
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

    # Test 3: backup.json exists and is valid JSON
    backup_path = os.path.join(SETUP_DIR, "backup.json")
    if not os.path.exists(backup_path):
        print(json.dumps({"test": "backup_exists", "passed": False, "message": "setup/backup.json does not exist"}))
        sys.exit(0)

    try:
        with open(backup_path, "r") as f:
            backup = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(json.dumps({"test": "backup_exists", "passed": False, "message": f"Could not parse backup.json: {e}"}))
        sys.exit(0)

    print(json.dumps({"test": "backup_exists", "passed": True, "message": "backup.json exists and is valid JSON"}))

    # Test 4: data.json matches backup.json (content equivalence)
    if data == backup:
        print(json.dumps({"test": "data_matches_backup", "passed": True, "message": "data.json content matches backup.json"}))
    else:
        print(json.dumps({"test": "data_matches_backup", "passed": False, "message": "data.json content does not match backup.json"}))

    # Test 5: data.checksum matches actual hash of data.json
    checksum_path = os.path.join(SETUP_DIR, "data.checksum")
    if not os.path.exists(checksum_path):
        print(json.dumps({"test": "checksum_valid", "passed": False, "message": "setup/data.checksum does not exist"}))
        sys.exit(0)

    with open(checksum_path, "r") as f:
        stored_checksum = f.read().strip()

    actual_checksum = hashlib.sha256(data_content.encode("utf-8")).hexdigest()

    if stored_checksum == actual_checksum:
        print(json.dumps({"test": "checksum_valid", "passed": True, "message": "data.checksum matches SHA-256 of data.json"}))
    else:
        print(json.dumps({"test": "checksum_valid", "passed": False, "message": f"Checksum mismatch: stored={stored_checksum}, actual={actual_checksum}"}))

    # Test 6: Charlie's role is 'viewer' (restored from backup, not tampered 'admin')
    charlie_role = None
    if isinstance(data, dict) and "users" in data:
        for user in data["users"]:
            if isinstance(user, dict) and user.get("name") == "Charlie":
                charlie_role = user.get("role")
                break

    if charlie_role == "viewer":
        print(json.dumps({"test": "tampering_fixed", "passed": True, "message": "Charlie's role is 'viewer' (corruption fixed)"}))
    else:
        print(json.dumps({"test": "tampering_fixed", "passed": False, "message": f"Expected Charlie's role = 'viewer', got '{charlie_role}'"}))


if __name__ == "__main__":
    main()
