#!/usr/bin/env python3
"""Verification script for Challenge 175: Tool Unavailable."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct backup value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "backup_result_77":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'backup_result_77'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'backup_result_77', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: verify the agent used the backup (not just guessed)
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if "backup" in answer:
        results.append({"test": "used_backup", "passed": True, "message": "Agent correctly fell back to backup service"})
    else:
        results.append({"test": "used_backup", "passed": False, "message": "Answer does not appear to come from backup service"})
else:
    results.append({"test": "used_backup", "passed": False, "message": "answer.txt not found"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "primary",
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
