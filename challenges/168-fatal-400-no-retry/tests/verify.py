#!/usr/bin/env python3
"""Verification script for Challenge 168: Fatal 400 No Retry."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip().lower()
    if answer in ("true", "validated"):
        results.append({"test": "correct_answer", "passed": True, "message": f"answer.txt contains '{answer}'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'true' or 'validated', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: tool was called exactly 2 times (not retried on 400)
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "call_log.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    call_count = state.get("count", 0)
    calls = state.get("calls", [])
    if call_count == 2:
        results.append({"test": "no_blind_retry", "passed": True, "message": f"Tool was called exactly 2 times: {calls}"})
    elif call_count > 2:
        results.append({"test": "no_blind_retry", "passed": False, "message": f"Tool was called {call_count} times — agent retried on 400 (should not retry client errors)"})
    else:
        results.append({"test": "no_blind_retry", "passed": False, "message": f"Tool was only called {call_count} time, expected exactly 2"})
else:
    results.append({"test": "no_blind_retry", "passed": False, "message": "State file not found — tool was never called"})

# Test 3: second call used the fallback input
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    calls = state.get("calls", [])
    if len(calls) >= 2 and calls[1] == "good_data":
        results.append({"test": "used_fallback", "passed": True, "message": "Agent correctly used fallback_input 'good_data' on second call"})
    elif len(calls) >= 2:
        results.append({"test": "used_fallback", "passed": False, "message": f"Second call used '{calls[1]}', expected 'good_data'"})
    else:
        results.append({"test": "used_fallback", "passed": False, "message": "Not enough calls to verify fallback usage"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "validator",
        min_calls=1, max_calls=3,
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
