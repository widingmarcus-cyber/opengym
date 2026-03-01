#!/usr/bin/env python3
"""Simulates an API with a latency spike on the first call.

First call: Sleeps for 3 seconds, then returns slow_result.
Second call and beyond: Returns immediately with fast_result.
Uses state file to track calls.
"""

import argparse
import json
import os
import time
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "api_calls.json")


def get_call_count():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("count", 0)
    return 0


def set_call_count(count):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"count": count}, f)


@audit_tool("slow_api")
def main():
    parser = argparse.ArgumentParser(description="Slow API simulator")
    parser.add_argument("--timeout", type=int, default=None,
                        help="Optional timeout in seconds")
    parser.parse_args()

    count = get_call_count()
    count += 1
    set_call_count(count)

    if count == 1:
        # Simulate latency spike
        time.sleep(3)
        response = {"data": "slow_result"}
    else:
        # Subsequent calls are fast
        response = {"data": "fast_result"}

    print(json.dumps(response))


if __name__ == "__main__":
    main()
