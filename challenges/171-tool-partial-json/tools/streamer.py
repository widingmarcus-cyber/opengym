#!/usr/bin/env python3
"""Simulates a streaming API that returns partial JSON on first call.

First call: Returns truncated JSON (not valid).
Second call: Returns complete, valid JSON.
Uses state file to track call count.
"""

import argparse
import json
import os
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "stream_count.json")


def get_count():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            return data.get("count", 0)
    return 0


def set_count(count):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"count": count}, f)


@audit_tool("streamer")
def main():
    parser = argparse.ArgumentParser(description="Streaming API simulator with partial JSON")
    parser.add_argument("--stream", action="store_true", help="Enable streaming mode")
    parser.parse_args()

    count = get_count()
    count += 1
    set_count(count)

    if count == 1:
        # Output truncated JSON (not valid)
        sys.stdout.write('{"data": [1, 2, 3')
        sys.stdout.flush()
    else:
        # Output complete JSON
        response = {"data": [1, 2, 3, 4, 5], "complete": True}
        print(json.dumps(response))


if __name__ == "__main__":
    main()
