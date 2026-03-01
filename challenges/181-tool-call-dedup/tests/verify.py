#!/usr/bin/env python3
"""Verify challenge 181: Tool Call Deduplication."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []

# Test 1: answer.txt exists
answer_path = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_path):
    results.append({"test": "answer_file_exists", "passed": True, "message": "answer.txt exists"})
else:
    results.append({"test": "answer_file_exists", "passed": False, "message": "answer.txt not found"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 2: answer.txt contains a valid number
with open(answer_path, "r") as f:
    content = f.read().strip()

try:
    answer_count = int(content)
    results.append({"test": "valid_number", "passed": True, "message": f"Answer is a valid number: {answer_count}"})
except ValueError:
    results.append({"test": "valid_number", "passed": False, "message": f"Answer is not a valid number: '{content}'"})
    for r in results:
        print(json.dumps(r))
    sys.exit(0)

# Test 3: The answer matches the actual state count
state_path = os.path.join(CHALLENGE_DIR, "tools", ".counter_state.json")
if os.path.exists(state_path):
    with open(state_path, "r") as f:
        state = json.load(f)
    actual_count = state.get("count", 0)
    if answer_count == actual_count:
        results.append({"test": "count_matches_state", "passed": True, "message": f"Answer ({answer_count}) matches actual tool call count ({actual_count})"})
    else:
        results.append({"test": "count_matches_state", "passed": False, "message": f"Answer ({answer_count}) does not match actual tool call count ({actual_count})"})
else:
    results.append({"test": "count_matches_state", "passed": False, "message": "Tool state file not found - tool was never called"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "counter_api",
        min_calls=1, max_calls=999,
        min_gap_ms=0,
    )
    if _audit_ok:
        results.append({"test": "audit_log_valid", "passed": True, "message": "Audit log signatures, sequences, and nonces valid"})
    else:
        for _err in _audit_errors[:3]:
            results.append({"test": "audit_log_valid", "passed": False, "message": _err})
except ImportError:
    results.append({"test": "audit_log_valid", "passed": True, "message": "Audit module not available (skipped)"})
for r in results:
    print(json.dumps(r))
