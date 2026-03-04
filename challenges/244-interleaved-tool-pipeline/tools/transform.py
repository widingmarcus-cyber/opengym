#!/usr/bin/env python3
"""Transform tool: multiplies each record's value by 2.

Usage: python3 tools/transform.py <input_file> <output_file>

Budget: 3 calls maximum.
"""

import json
import os
import sys

STATE_DIR = os.path.join(os.path.dirname(__file__), ".state")
STATE_FILE = os.path.join(STATE_DIR, "transform_calls.json")
BUDGET = 3


def load_call_log():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return []


def save_call_log(log):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(log, f, indent=2)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 tools/transform.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    call_log = load_call_log()

    if len(call_log) >= BUDGET:
        print(f"ERROR: transform budget exceeded ({BUDGET} calls max, already made {len(call_log)})", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        records = json.load(f)

    transformed = []
    for record in records:
        result = dict(record)
        result["value"] = record["value"] * 2
        result["transformed"] = True
        transformed.append(result)

    with open(output_file, "w") as f:
        json.dump(transformed, f, indent=2)

    call_log.append({
        "call_number": len(call_log) + 1,
        "input": input_file,
        "output": output_file,
        "records_processed": len(records)
    })
    save_call_log(call_log)

    print(f"transform: processed {len(records)} records (call {len(call_log)}/{BUDGET})")


if __name__ == "__main__":
    main()
