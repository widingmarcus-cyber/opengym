#!/usr/bin/env python3
"""An API tool with a quota of 5 calls per session. Supports batch queries."""

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

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".quota_state.json")

QUOTA_LIMIT = 5


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"call_count": 0}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_result(query):
    """Generate a deterministic result for a query."""
    results_map = {
        "q1": "r1",
        "q2": "r2",
        "q3": "r3",
        "q4": "r4",
        "q5": "r5",
        "q6": "r6",
        "q7": "r7",
        "q8": "r8",
    }
    return results_map.get(query, f"result_for_{query}")


@audit_tool("quota_api")
def main():
    parser = argparse.ArgumentParser(description="Quota-limited API tool")
    parser.add_argument("--query", help="Single query to execute")
    parser.add_argument("--batch", help="Comma-separated batch of queries (up to 3)")
    args = parser.parse_args()

    if not args.query and not args.batch:
        print(json.dumps({"error": "Provide --query or --batch argument"}))
        sys.exit(1)

    state = load_state()
    state["call_count"] += 1
    remaining = QUOTA_LIMIT - state["call_count"]
    save_state(state)

    if state["call_count"] > QUOTA_LIMIT:
        response = {
            "status": 429,
            "error": "Quota exhausted",
            "remaining_quota": 0
        }
        print(json.dumps(response))
        return

    if args.batch:
        queries = [q.strip() for q in args.batch.split(",")]
        if len(queries) > 3:
            print(json.dumps({"error": "Batch size exceeds maximum of 3"}))
            return
        batch_results = {}
        for q in queries:
            batch_results[q] = get_result(q)
        response = {
            "status": 200,
            "results": batch_results,
            "remaining_quota": max(0, remaining)
        }
    else:
        response = {
            "status": 200,
            "data": get_result(args.query),
            "query": args.query,
            "remaining_quota": max(0, remaining)
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
