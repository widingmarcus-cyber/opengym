#!/usr/bin/env python3
"""Verification script for Challenge 173: Tool Latency Spike."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = []

# Test 1: answer.txt exists and contains the slow result
answer_file = os.path.join(CHALLENGE_DIR, "setup", "answer.txt")
if os.path.exists(answer_file):
    with open(answer_file, "r") as f:
        answer = f.read().strip()
    if answer == "slow_result":
        results.append({"test": "waited_for_slow", "passed": True, "message": "answer.txt contains 'slow_result' — agent waited for the slow response"})
    elif answer == "fast_result":
        results.append({"test": "waited_for_slow", "passed": False, "message": "answer.txt contains 'fast_result' — agent gave up on slow call and used second (fast) result"})
    else:
        results.append({"test": "waited_for_slow", "passed": False, "message": f"Expected 'slow_result', got '{answer}'"})
else:
    results.append({"test": "waited_for_slow", "passed": False, "message": "answer.txt not found"})

# Test 2: check call count (ideally 1 — agent waited patiently)
state_file = os.path.join(CHALLENGE_DIR, "tools", ".state", "api_calls.json")
if os.path.exists(state_file):
    with open(state_file, "r") as f:
        state = json.load(f)
    count = state.get("count", 0)
    if count == 1:
        results.append({"test": "single_call", "passed": True, "message": "API was called once — agent waited patiently for the slow response"})
    else:
        results.append({"test": "single_call", "passed": True, "message": f"API was called {count} times — agent retried but still got the correct result"})
else:
    results.append({"test": "single_call", "passed": False, "message": "State file not found — API was never called"})

for r in results:
    print(json.dumps(r))
