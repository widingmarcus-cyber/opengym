#!/usr/bin/env python3
"""Lookup tool with budget constraints.

Usage:
    python tools/lookup.py "apple,banana,cherry"

Looks up 1-3 items per call. Maximum 5 total calls (tracked in .state/budget.json).
"""

import json
import os
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(TOOL_DIR, ".state", "budget.json")

# Item database
ITEMS_DB = {
    "apple": {"category": "fruit", "color": "red", "calories": 95},
    "banana": {"category": "fruit", "color": "yellow", "calories": 105},
    "cherry": {"category": "fruit", "color": "red", "calories": 77},
    "date": {"category": "fruit", "color": "brown", "calories": 282},
    "elderberry": {"category": "berry", "color": "purple", "calories": 73},
    "fig": {"category": "fruit", "color": "purple", "calories": 74},
    "grape": {"category": "fruit", "color": "green", "calories": 62},
    "honeydew": {"category": "melon", "color": "green", "calories": 64},
    "kiwi": {"category": "fruit", "color": "brown", "calories": 42},
    "lemon": {"category": "citrus", "color": "yellow", "calories": 17},
}


def load_budget():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    return {"calls": 0, "max_calls": 5}


def save_budget(budget):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(budget, f, indent=2)


@audit_tool("lookup")
def main():
    if len(sys.argv) < 2:
        print("Usage: python lookup.py \"item1,item2,item3\"", file=sys.stderr)
        print("Max 3 items per call, max 5 calls total.", file=sys.stderr)
        sys.exit(1)

    # Parse items
    items_input = sys.argv[1]
    items = [item.strip().lower() for item in items_input.split(",") if item.strip()]

    if len(items) == 0:
        print("Error: No items provided.", file=sys.stderr)
        sys.exit(1)

    if len(items) > 3:
        print("Error: Maximum 3 items per call. You provided {}.".format(len(items)), file=sys.stderr)
        sys.exit(1)

    # Check budget
    budget = load_budget()
    if budget["calls"] >= budget["max_calls"]:
        print("Error: Budget exhausted! {} of {} calls used.".format(
            budget["calls"], budget["max_calls"]
        ), file=sys.stderr)
        sys.exit(1)

    # Increment call count
    budget["calls"] += 1
    save_budget(budget)

    # Look up items
    result = {}
    for item in items:
        if item in ITEMS_DB:
            result[item] = ITEMS_DB[item]
        else:
            result[item] = {"error": "Item not found"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
