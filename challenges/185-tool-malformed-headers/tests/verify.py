#!/usr/bin/env python3
"""Verify challenge 185: Tool Malformed Headers."""

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

# Test 2: answer.txt contains "valid_result_88"
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "valid_result_88":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data extracted: valid_result_88"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'valid_result_88', got '{content}'"})

# Test 3: Agent did not include WARNING lines in the answer
if "WARNING" not in content:
    results.append({"test": "no_warnings_in_answer", "passed": True, "message": "Answer does not contain warning text"})
else:
    results.append({"test": "no_warnings_in_answer", "passed": False, "message": "Answer contains WARNING text that should have been filtered"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "buggy_api",
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
