#!/usr/bin/env python3
"""Simulates a service that returns a transient 500 error on first call.

First call: HTTP 500 Internal Server Error.
Second call and beyond: HTTP 200 with recovered data.
"""

import argparse
import json
import os
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "attempts.json")


def get_attempts():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("attempts", 0)
    return 0


def set_attempts(count):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"attempts": count}, f)


@audit_tool("service")
def main():
    parser = argparse.ArgumentParser(description="Transient failure service simulator")
    parser.add_argument("--endpoint", default="/data", help="Service endpoint")
    parser.parse_args()

    attempts = get_attempts()
    attempts += 1
    set_attempts(attempts)

    if attempts == 1:
        response = {
            "status": 500,
            "error": "Internal Server Error"
        }
    else:
        response = {
            "status": 200,
            "data": {"value": "recovered_result"}
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
