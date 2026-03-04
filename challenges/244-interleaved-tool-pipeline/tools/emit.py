#!/usr/bin/env python3
"""Emit tool: appends processed records to the final output file.

Usage: python3 tools/emit.py <input_file> <output_file>

The output_file should be setup/output.json. Records are appended
(not overwritten) so multiple emit calls accumulate results.

Budget: 2 calls maximum.
"""

import json
import os
import sys

STATE_DIR = os.path.join(os.path.dirname(__file__), ".state")
STATE_FILE = os.path.join(STATE_DIR, "emit_calls.json")
BUDGET = 2


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
        print("Usage: python3 tools/emit.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    call_log = load_call_log()

    if len(call_log) >= BUDGET:
        print(f"ERROR: emit budget exceeded ({BUDGET} calls max, already made {len(call_log)})", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        new_records = json.load(f)

    # Append to existing output if it exists
    existing = []
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            existing = json.load(f)

    combined = existing + new_records

    with open(output_file, "w") as f:
        json.dump(combined, f, indent=2)

    call_log.append({
        "call_number": len(call_log) + 1,
        "input": input_file,
        "output": output_file,
        "records_emitted": len(new_records),
        "total_records": len(combined)
    })
    save_call_log(call_log)

    print(f"emit: wrote {len(new_records)} records, total now {len(combined)} (call {len(call_log)}/{BUDGET})")


if __name__ == "__main__":
    main()
