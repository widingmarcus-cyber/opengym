#!/usr/bin/env python3
"""Simulates an input validator that rejects bad data with HTTP 400.

If input is "bad_data", returns 400 (client error — should not be retried).
If input is "good_data", returns 200 with validated result.
Tracks call count in state file.
"""

import argparse
import json
import os

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "call_log.json")


def log_call(input_value):
    os.makedirs(STATE_DIR, exist_ok=True)
    calls = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            calls = data.get("calls", [])
    calls.append(input_value)
    with open(STATE_FILE, "w") as f:
        json.dump({"calls": calls, "count": len(calls)}, f)


def main():
    parser = argparse.ArgumentParser(description="Input validator simulator")
    parser.add_argument("--input", required=True, help="Input data to validate")
    args = parser.parse_args()

    log_call(args.input)

    if args.input == "bad_data":
        response = {
            "status": 400,
            "error": "Invalid input: bad_data"
        }
    elif args.input == "good_data":
        response = {
            "status": 200,
            "data": {"validated": True}
        }
    else:
        response = {
            "status": 400,
            "error": f"Unknown input: {args.input}"
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
