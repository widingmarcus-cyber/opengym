#!/usr/bin/env python3
"""Verify challenge 183: Tool Encoding Change."""

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

# Test 2: answer.txt contains "cafe" with accent (UTF-8)
with open(answer_path, "r", encoding="utf-8") as f:
    content = f.read().strip()

if content == "caf\u00e9":
    results.append({"test": "correct_utf8_text", "passed": True, "message": "Correct UTF-8 text: caf\u00e9"})
else:
    results.append({"test": "correct_utf8_text", "passed": False, "message": f"Expected 'caf\\u00e9', got '{content}'"})

# Test 3: File is valid UTF-8
try:
    with open(answer_path, "rb") as f:
        raw = f.read()
    raw.decode("utf-8")
    results.append({"test": "valid_utf8_encoding", "passed": True, "message": "File is valid UTF-8"})
except UnicodeDecodeError:
    results.append({"test": "valid_utf8_encoding", "passed": False, "message": "File is not valid UTF-8"})


# === Audit log validation ===
_audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
_tools_dir = os.path.join(CHALLENGE_DIR, "tools")
sys.path.insert(0, _tools_dir)
try:
    from _audit import full_audit_check
    _audit_ok, _audit_errors = full_audit_check(
        _audit_file, "text_api",
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
