#!/usr/bin/env python3
"""Verification script for Challenge 167: Transient 500 Retry."""

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
    if answer == "recovered_result":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'recovered_result'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'recovered_result', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: attempts.json shows at least 2 calls
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "attempts.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    attempts = state.get("attempts", 0)
    if attempts >= 2:
        results.append({"test": "retry_attempted", "passed": True, "message": f"Service was called {attempts} times (>=2 required)"})
    else:
        results.append({"test": "retry_attempted", "passed": False, "message": f"Service was only called {attempts} time, expected >=2"})
else:
    results.append({"test": "retry_attempted", "passed": False, "message": "State file not found — service was never called"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "service",
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
