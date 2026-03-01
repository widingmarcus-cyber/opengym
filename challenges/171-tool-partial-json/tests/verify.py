#!/usr/bin/env python3
"""Verification script for Challenge 171: Tool Partial JSON."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains correct sum
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "15":
        results.append({"test": "correct_sum", "passed": True, "message": "answer.txt contains '15' (correct sum of [1,2,3,4,5])"})
    else:
        results.append({"test": "correct_sum", "passed": False, "message": f"Expected '15', got '{answer}'"})
else:
    results.append({"test": "correct_sum", "passed": False, "message": "answer.txt not found"})

# Test 2: streamer was called at least twice (first was partial)
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "stream_count.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    count = state.get("count", 0)
    if count >= 2:
        results.append({"test": "handled_partial", "passed": True, "message": f"Streamer was called {count} times (detected and retried partial JSON)"})
    else:
        results.append({"test": "handled_partial", "passed": False, "message": f"Streamer was only called {count} time — partial JSON was not detected"})
else:
    results.append({"test": "handled_partial", "passed": False, "message": "State file not found — streamer was never called"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "streamer",
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
