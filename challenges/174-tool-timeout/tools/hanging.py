#!/usr/bin/env python3
"""Simulates a tool that times out on first call.

First call (no flags): Sleeps 2 seconds then returns timeout error.
Call with --fallback: Returns immediately with fallback data.
Call with --timeout N: Sleeps N seconds then returns timeout error.
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
STATE_FILE = os.path.join(STATE_DIR, "hang_state.json")


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


@audit_tool("hanging")
def main():
    parser = argparse.ArgumentParser(description="Hanging tool simulator")
    parser.add_argument("--timeout", type=int, default=None,
                        help="Timeout in seconds before returning error")
    parser.add_argument("--fallback", action="store_true",
                        help="Use fallback mode (returns immediately)")
    args = parser.parse_args()

    count = get_call_count()
    count += 1
    set_call_count(count)

    if args.fallback:
        # Fallback mode: return immediately
        response = {"status": "ok", "data": "fallback_value"}
        print(json.dumps(response))
        return

    if args.timeout is not None:
        # Custom timeout
        time.sleep(min(args.timeout, 2))
        response = {"status": "timeout", "error": "Operation timed out"}
        print(json.dumps(response))
        return

    # Default: simulate timeout on first call
    time.sleep(2)
    response = {"status": "timeout", "error": "Operation timed out"}
    print(json.dumps(response))


if __name__ == "__main__":
    main()
