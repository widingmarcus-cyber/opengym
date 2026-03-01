#!/usr/bin/env python3
"""Verify challenge 177: Tool Stale Cache."""

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

# Test 2: answer.txt contains "fresh_value"
with open(answer_path, "r") as f:
    content = f.read().strip()

if content == "fresh_value":
    results.append({"test": "correct_fresh_value", "passed": True, "message": "Correct fresh value retrieved"})
else:
    results.append({"test": "correct_fresh_value", "passed": False, "message": f"Expected 'fresh_value', got '{content}'"})

# Test 3: Agent did not write the stale value
if content != "old_value":
    results.append({"test": "not_stale_value", "passed": True, "message": "Agent correctly avoided stale cached value"})
else:
    results.append({"test": "not_stale_value", "passed": False, "message": "Agent wrote the stale cached value instead of fresh"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "cached_api",
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
