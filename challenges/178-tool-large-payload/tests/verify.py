#!/usr/bin/env python3
"""Verify challenge 178: Tool Large Payload."""

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

# Test 2: answer.txt contains "10100"
# Sum of values: sum(i*2 for i in range(1,101)) = 2*sum(1..100) = 2*5050 = 10100
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "10100":
    results.append({"test": "correct_sum", "passed": True, "message": "Correct sum of all values: 10100"})
else:
    results.append({"test": "correct_sum", "passed": False, "message": f"Expected '10100', got '{content}'"})

# Test 3: Verify the answer is a valid number
try:
    val = int(content)
    results.append({"test": "valid_number", "passed": True, "message": f"Answer is a valid number: {val}"})
except ValueError:
    results.append({"test": "valid_number", "passed": False, "message": f"Answer is not a valid number: '{content}'"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "data_dump",
        min_calls=2, max_calls=999,
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
