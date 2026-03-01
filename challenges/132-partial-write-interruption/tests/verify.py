#!/usr/bin/env python3
"""Verification script for Challenge 132: Partial Write Interruption"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

# Test 1: data.json exists and is valid JSON
data_path = os.path.join(SETUP_DIR, "data.json")
if not os.path.exists(data_path):
    print(json.dumps({"test": "data_file_exists", "passed": False, "message": "data.json does not exist"}))
    sys.exit(0)

try:
    with open(data_path, "r") as f:
        data = json.load(f)
    print(json.dumps({"test": "data_file_exists", "passed": True, "message": "data.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "data_file_exists", "passed": False, "message": f"data.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: data.json contains exactly 10 records
if isinstance(data, list):
    if len(data) == 10:
        print(json.dumps({"test": "record_count", "passed": True, "message": "data.json contains exactly 10 records"}))
    else:
        print(json.dumps({"test": "record_count", "passed": False, "message": f"Expected 10 records, found {len(data)}"}))
else:
    print(json.dumps({"test": "record_count", "passed": False, "message": "data.json is not a JSON array"}))
    sys.exit(0)

# Test 3: Record 3 (id=3) has been repaired -- value field contains temperature, humidity, and pressure
record_3 = None
for record in data:
    if isinstance(record, dict) and record.get("id") == 3:
        record_3 = record
        break

if record_3 is None:
    print(json.dumps({"test": "record_3_fixed", "passed": False, "message": "Record with id=3 not found"}))
else:
    value = record_3.get("value", "")
    has_temperature = "temperature:" in value
    has_humidity = "humidity:" in value
    has_pressure = "pressure:" in value
    if has_temperature and has_humidity and has_pressure:
        print(json.dumps({"test": "record_3_fixed", "passed": True, "message": f"Record 3 has been repaired: '{value}'"}))
    else:
        missing = []
        if not has_temperature:
            missing.append("temperature")
        if not has_humidity:
            missing.append("humidity")
        if not has_pressure:
            missing.append("pressure")
        print(json.dumps({"test": "record_3_fixed", "passed": False, "message": f"Record 3 value is still incomplete. Missing: {', '.join(missing)}. Value: '{value}'"}))

# Test 4: All 10 records have valid structure (id, name, value with all three fields)
valid_count = 0
invalid_records = []
for record in data:
    if not isinstance(record, dict):
        invalid_records.append(f"Non-dict entry found: {record}")
        continue
    rid = record.get("id")
    name = record.get("name")
    value = record.get("value", "")
    if rid is None:
        invalid_records.append(f"Record missing 'id': {record}")
    elif not isinstance(name, str) or not name:
        invalid_records.append(f"Record {rid} missing or empty 'name'")
    elif not isinstance(value, str):
        invalid_records.append(f"Record {rid} 'value' is not a string")
    elif "temperature:" not in value or "humidity:" not in value or "pressure:" not in value:
        invalid_records.append(f"Record {rid} has incomplete value: '{value}'")
    else:
        valid_count += 1

if valid_count == 10:
    print(json.dumps({"test": "all_records_valid", "passed": True, "message": "All 10 records have valid structure with complete value fields"}))
else:
    print(json.dumps({"test": "all_records_valid", "passed": False, "message": f"{valid_count}/10 records valid. Issues: {'; '.join(invalid_records)}"}))

# Test 5: IDs 1-10 are all present
found_ids = set()
for record in data:
    if isinstance(record, dict) and "id" in record:
        found_ids.add(record["id"])

expected_ids = set(range(1, 11))
missing_ids = expected_ids - found_ids
if not missing_ids:
    print(json.dumps({"test": "all_ids_present", "passed": True, "message": "All IDs 1-10 are present"}))
else:
    print(json.dumps({"test": "all_ids_present", "passed": False, "message": f"Missing IDs: {sorted(missing_ids)}"}))

# Test 6: answer.txt exists and contains "10"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "10":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains exactly '10'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '10' in answer.txt, got '{answer}'"}))
