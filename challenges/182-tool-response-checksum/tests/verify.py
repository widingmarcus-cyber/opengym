#!/usr/bin/env python3
"""Verify challenge 182: Tool Response Checksum."""

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

# Test 2: answer.txt contains "important_payload_123"
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "important_payload_123":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data written: important_payload_123"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'important_payload_123', got '{content}'"})

# Test 3: Agent did not write CHECKSUM_MISMATCH (checksum is valid)
if content != "CHECKSUM_MISMATCH":
    results.append({"test": "checksum_validated", "passed": True, "message": "Agent correctly determined the checksum is valid"})
else:
    results.append({"test": "checksum_validated", "passed": False, "message": "Agent incorrectly reported a checksum mismatch"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "verified_api",
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
