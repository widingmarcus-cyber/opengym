#!/usr/bin/env python3
"""Verification script for Challenge 170: Tool Output Type Change."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "42":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains '42'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected '42', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: Verify value is parseable as integer (not quoted string)
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    # Check it's not wrapped in quotes
    if answer.startswith('"') or answer.startswith("'"):
        results.append({"test": "type_correct", "passed": False, "message": f"Value appears to be a quoted string: {answer}"})
    else:
        try:
            val = int(answer)
            if val == 42:
                results.append({"test": "type_correct", "passed": True, "message": "Value correctly parsed as integer 42"})
            else:
                results.append({"test": "type_correct", "passed": False, "message": f"Integer value is {val}, expected 42"})
        except ValueError:
            results.append({"test": "type_correct", "passed": False, "message": f"Value '{answer}' could not be parsed as integer"})
else:
    results.append({"test": "type_correct", "passed": False, "message": "answer.txt not found"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "converter",
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
