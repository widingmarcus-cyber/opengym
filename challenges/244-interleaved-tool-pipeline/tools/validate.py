#!/usr/bin/env python3
"""Validate tool: checks that all record values are positive.

Usage: python3 tools/validate.py <input_file> <output_file>

Budget: 3 calls maximum.
"""

import json
import os
import sys

STATE_DIR = os.path.join(os.path.dirname(__file__), ".state")
STATE_FILE = os.path.join(STATE_DIR, "validate_calls.json")
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
        print("Usage: python3 tools/validate.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    call_log = load_call_log()

    if len(call_log) >= BUDGET:
        print(f"ERROR: validate budget exceeded ({BUDGET} calls max, already made {len(call_log)})", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        records = json.load(f)

    validated = []
    all_valid = True
    for record in records:
        is_valid = isinstance(record.get("value"), (int, float)) and record["value"] > 0
        result = dict(record)
        result["validated"] = True
        result["valid"] = is_valid
        if not is_valid:
            all_valid = False
        validated.append(result)

    with open(output_file, "w") as f:
        json.dump(validated, f, indent=2)

    call_log.append({
        "call_number": len(call_log) + 1,
        "input": input_file,
        "output": output_file,
        "records_processed": len(records),
        "all_valid": all_valid
    })
    save_call_log(call_log)

    status = "PASS" if all_valid else "FAIL"
    print(f"validate: {status} - processed {len(records)} records (call {len(call_log)}/{BUDGET})")


if __name__ == "__main__":
    main()
