#!/usr/bin/env python3
"""Verification script for Challenge 129: Versioned Memory Retrieval"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")

EXPECTED_VERSIONS = {
    1: "alpha",
    2: "beta",
    3: "gamma",
}

# Test 1: memory.json exists and is valid JSON
memory_path = os.path.join(SETUP_DIR, "memory.json")
if not os.path.exists(memory_path):
    print(json.dumps({"test": "memory_file_exists", "passed": False, "message": "memory.json does not exist"}))
    sys.exit(0)

try:
    with open(memory_path, "r") as f:
        memory = json.load(f)
    print(json.dumps({"test": "memory_file_exists", "passed": True, "message": "memory.json exists and is valid JSON"}))
except (json.JSONDecodeError, IOError) as e:
    print(json.dumps({"test": "memory_file_exists", "passed": False, "message": f"memory.json is not valid JSON: {e}"}))
    sys.exit(0)

# Test 2: memory.json contains all 3 versioned entries
# Support multiple formats: list of dicts, or dict with nested structure
found_versions = {}

if isinstance(memory, list):
    for entry in memory:
        if isinstance(entry, dict):
            key = entry.get("key", "")
            version = entry.get("version")
            value = entry.get("value")
            if key == "config" and version is not None:
                found_versions[int(version)] = value
elif isinstance(memory, dict):
    # Support dict format like {"config": {"1": "alpha", ...}} or {"config": [{"version": 1, ...}]}
    config_data = memory.get("config", memory)
    if isinstance(config_data, list):
        for entry in config_data:
            if isinstance(entry, dict):
                version = entry.get("version")
                value = entry.get("value")
                if version is not None:
                    found_versions[int(version)] = value
    elif isinstance(config_data, dict):
        for k, v in config_data.items():
            try:
                found_versions[int(k)] = v
            except (ValueError, TypeError):
                pass

missing = []
wrong = []
for ver, expected_val in EXPECTED_VERSIONS.items():
    if ver not in found_versions:
        missing.append(f"version {ver}")
    elif found_versions[ver] != expected_val:
        wrong.append(f"version {ver}: expected '{expected_val}', got '{found_versions[ver]}'")

if not missing and not wrong:
    print(json.dumps({"test": "all_versions_stored", "passed": True, "message": "All 3 versioned entries found with correct values"}))
else:
    issues = []
    if missing:
        issues.append(f"Missing: {', '.join(missing)}")
    if wrong:
        issues.append(f"Wrong values: {'; '.join(wrong)}")
    print(json.dumps({"test": "all_versions_stored", "passed": False, "message": "; ".join(issues)}))

# Test 3: answer.txt exists and contains "beta"
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == "beta":
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains exactly 'beta'"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected 'beta' in answer.txt, got '{answer}'"}))
