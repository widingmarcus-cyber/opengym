#!/usr/bin/env python3
"""A counter API tool that tracks call count in persistent state."""

import argparse
import json
import os

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".counter_state.json")


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"count": 0, "actions": []}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def main():
    parser = argparse.ArgumentParser(description="Counter API tool")
    parser.add_argument("--action", required=True, help="Action to perform")
    args = parser.parse_args()

    state = load_state()
    state["count"] += 1
    state["actions"].append(args.action)
    save_state(state)

    response = {
        "count": state["count"],
        "action": args.action,
        "status": "processed"
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
