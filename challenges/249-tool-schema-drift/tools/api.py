#!/usr/bin/env python3
"""API tool that returns item data with schema drift across calls.

Usage: python3 tools/api.py <item_name>

The response schema changes based on cumulative call count:
  - Calls 1-3: v1 format
  - Calls 4-6: v2 format
  - Calls 7-8: v3 format

Call state is persisted in tools/.state/api_calls.json.
"""

import json
import os
import sys

# Hardcoded price list for deterministic results
PRICE_LIST = {
    "laptop":     {"value": 999.99, "in_stock": True},
    "keyboard":   {"value": 79.99,  "in_stock": True},
    "mouse":      {"value": 49.99,  "in_stock": True},
    "monitor":    {"value": 399.99, "in_stock": True},
    "headset":    {"value": 149.99, "in_stock": True},
    "webcam":     {"value": 89.99,  "in_stock": True},
    "microphone": {"value": 129.99, "in_stock": False},
    "speaker":    {"value": 199.99, "in_stock": True},
}

STATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".state")
STATE_FILE = os.path.join(STATE_DIR, "api_calls.json")


def get_call_count():
    """Read and increment the call counter."""
    os.makedirs(STATE_DIR, exist_ok=True)
    if os.path.isfile(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {"call_count": 0}

    state["call_count"] += 1
    call_num = state["call_count"]

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

    return call_num


def format_v1(item_name, item_data):
    """Schema v1: calls 1-3."""
    return {
        "name": item_name,
        "value": item_data["value"],
        "in_stock": item_data["in_stock"],
    }


def format_v2(item_name, item_data):
    """Schema v2: calls 4-6."""
    print("SCHEMA_VERSION: v2", file=sys.stderr)
    return {
        "item_name": item_name,
        "item_value": item_data["value"],
        "available": item_data["in_stock"],
        "unit": "USD",
    }


def format_v3(item_name, item_data):
    """Schema v3: calls 7-8."""
    print("SCHEMA_VERSION: v3", file=sys.stderr)
    return {
        "n": item_name,
        "v": item_data["value"],
        "s": item_data["in_stock"],
        "u": "USD",
        "deprecated": True,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tools/api.py <item_name>", file=sys.stderr)
        sys.exit(1)

    item_name = sys.argv[1].strip().lower()

    if item_name not in PRICE_LIST:
        print(json.dumps({"error": f"Unknown item: {item_name}"}))
        sys.exit(1)

    item_data = PRICE_LIST[item_name]
    call_num = get_call_count()

    if call_num <= 3:
        result = format_v1(item_name, item_data)
    elif call_num <= 6:
        result = format_v2(item_name, item_data)
    else:
        result = format_v3(item_name, item_data)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
