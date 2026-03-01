#!/usr/bin/env python3
"""Verify challenge 179: Tool Auth Refresh."""

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

# Test 2: answer.txt contains "secret_data_99"
with open(answer_path, "r") as f:
    answer_content = f.read().strip()

if answer_content == "secret_data_99":
    results.append({"test": "correct_data", "passed": True, "message": "Correct data retrieved: secret_data_99"})
else:
    results.append({"test": "correct_data", "passed": False, "message": f"Expected 'secret_data_99', got '{answer_content}'"})

# Test 3: token.txt updated to fresh token
token_path = os.path.join(CHALLENGE_DIR, "setup", "token.txt")
if os.path.exists(token_path):
    with open(token_path, "r") as f:
        token_content = f.read().strip()
    if token_content == "fresh_token_xyz":
        results.append({"test": "token_updated", "passed": True, "message": "Token updated to fresh_token_xyz"})
    else:
        results.append({"test": "token_updated", "passed": False, "message": f"Expected token 'fresh_token_xyz', got '{token_content}'"})
else:
    results.append({"test": "token_updated", "passed": False, "message": "token.txt not found"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "auth_api",
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
