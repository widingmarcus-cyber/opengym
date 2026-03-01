#!/usr/bin/env python3
"""Verification script for Challenge 105: Knowledge Update"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: answers.json exists
answers_path = os.path.join(SETUP_DIR, "answers.json")
if os.path.exists(answers_path):
    print(json.dumps({"test": "answers_file_exists", "passed": True, "message": "answers.json exists"}))
else:
    print(json.dumps({"test": "answers_file_exists", "passed": False, "message": "answers.json does not exist"}))
    sys.exit(0)

# Load answers
try:
    with open(answers_path, "r") as f:
        answers = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "answers_valid_json", "passed": False, "message": f"answers.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: Alice's office is UPDATED to Building C, Room 112
alice_office = answers.get("alice_office", "").strip()
if "Building C" in alice_office and "112" in alice_office:
    print(json.dumps({"test": "alice_office_updated", "passed": True, "message": f"Alice's office correctly updated to '{alice_office}'"}))
else:
    print(json.dumps({"test": "alice_office_updated", "passed": False, "message": f"Alice's office should be 'Building C, Room 112' (updated), got '{alice_office}'"}))

# Test 3: Carol's role is UPDATED to VP of Engineering
carol_role = answers.get("carol_role", "").strip()
if "VP" in carol_role.upper() and "ENGINEERING" in carol_role.upper():
    print(json.dumps({"test": "carol_role_updated", "passed": True, "message": f"Carol's role correctly updated to '{carol_role}'"}))
else:
    print(json.dumps({"test": "carol_role_updated", "passed": False, "message": f"Carol's role should be 'VP of Engineering' (updated), got '{carol_role}'"}))

# Test 4: Dave's status indicates departure
dave_status = answers.get("dave_status", "").strip().lower()
departed_indicators = ["departed", "left", "removed", "gone", "inactive", "no longer", "not active"]
if any(indicator in dave_status for indicator in departed_indicators):
    print(json.dumps({"test": "dave_departed", "passed": True, "message": f"Dave correctly marked as departed: '{dave_status}'"}))
else:
    print(json.dumps({"test": "dave_departed", "passed": False, "message": f"Dave should be marked as departed/left, got '{dave_status}'"}))

# Test 5: Iris's extension is 5009 (new hire)
iris_extension = str(answers.get("iris_extension", "")).strip()
if iris_extension == "5009":
    print(json.dumps({"test": "iris_extension", "passed": True, "message": "Iris's extension correctly set to 5009"}))
else:
    print(json.dumps({"test": "iris_extension", "passed": False, "message": f"Iris's extension should be '5009' (new hire), got '{iris_extension}'"}))

# Test 6: Bob's office is UNCHANGED at Building B, Room 102
bob_office = answers.get("bob_office", "").strip()
if "Building B" in bob_office and "102" in bob_office:
    print(json.dumps({"test": "bob_office_unchanged", "passed": True, "message": f"Bob's office correctly unchanged at '{bob_office}'"}))
else:
    print(json.dumps({"test": "bob_office_unchanged", "passed": False, "message": f"Bob's office should be 'Building B, Room 102' (unchanged), got '{bob_office}'"}))

# Test 7: Total active members is 8 (original 8 - Dave + Iris = 8)
total = answers.get("total_active_members")
if total is not None:
    try:
        total = int(total)
    except (ValueError, TypeError):
        print(json.dumps({"test": "total_active_members", "passed": False, "message": f"total_active_members should be a number, got '{total}'"}))
        sys.exit(0)
    if total == 8:
        print(json.dumps({"test": "total_active_members", "passed": True, "message": "Total active members correctly calculated as 8 (8 - Dave + Iris)"}))
    else:
        print(json.dumps({"test": "total_active_members", "passed": False, "message": f"Total active members should be 8 (original 8 - Dave + Iris), got {total}"}))
else:
    print(json.dumps({"test": "total_active_members", "passed": False, "message": "total_active_members field is missing from answers"}))
