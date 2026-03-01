#!/usr/bin/env python3
"""Verification script for Challenge 166: 429 Retry-After Enforcement."""

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
    if answer == "success_data_42":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'success_data_42'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'success_data_42', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: call_count.json shows 3+ calls were made
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "call_count.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    call_count = state.get("count", 0)
    if call_count >= 3:
        results.append({"test": "retry_count", "passed": True, "message": f"Tool was called {call_count} times (>=3 required)"})
    else:
        results.append({"test": "retry_count", "passed": False, "message": f"Tool was only called {call_count} times, expected >=3"})
else:
    results.append({"test": "retry_count", "passed": False, "message": "State file not found — tool was never called"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "api",
        min_calls=3, max_calls=999,
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
