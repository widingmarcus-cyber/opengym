#!/usr/bin/env python3
"""Simulates a rate-limited API endpoint.

First 2 calls return HTTP 429 with Retry-After header.
Third call returns HTTP 200 with success data.
"""

import argparse
import json
import os

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "call_count.json")


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


def main():
    parser = argparse.ArgumentParser(description="Rate-limited API simulator")
    parser.add_argument("--endpoint", default="/data", help="API endpoint to call")
    parser.parse_args()

    count = get_call_count()
    count += 1
    set_call_count(count)

    if count <= 2:
        response = {
            "status": 429,
            "headers": {"Retry-After": "1"},
            "body": None
        }
    else:
        response = {
            "status": 200,
            "headers": {},
            "body": {"result": "success_data_42"}
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
