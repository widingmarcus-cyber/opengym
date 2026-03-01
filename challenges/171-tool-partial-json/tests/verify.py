#!/usr/bin/env python3
"""Verification script for Challenge 171: Tool Partial JSON."""

import json
import os

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

for r in results:
    print(json.dumps(r))
