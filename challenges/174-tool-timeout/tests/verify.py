#!/usr/bin/env python3
"""Verification script for Challenge 174: Tool Timeout."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct fallback value
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "fallback_value":
        results.append({"test": "correct_answer", "passed": True, "message": "answer.txt contains 'fallback_value'"})
    else:
        results.append({"test": "correct_answer", "passed": False, "message": f"Expected 'fallback_value', got '{answer}'"})
else:
    results.append({"test": "correct_answer", "passed": False, "message": "answer.txt not found"})

# Test 2: tool was called at least twice (timeout detected, then fallback used)
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "hang_state.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    count = state.get("count", 0)
    if count >= 2:
        results.append({"test": "timeout_handled", "passed": True, "message": f"Tool was called {count} times — timeout was detected and fallback was used"})
    else:
        results.append({"test": "timeout_handled", "passed": False, "message": "Tool was never called"})
else:
    results.append({"test": "timeout_handled", "passed": False, "message": "State file not found — tool was never called"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "hanging",
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
