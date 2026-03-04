#!/usr/bin/env python3
"""Enrich tool: adds enrichment metadata to each record.

Usage: python3 tools/enrich.py <input_file> <output_file>

Budget: 2 calls maximum.
"""

import json
import os
import sys
from datetime import datetime, timezone

STATE_DIR = os.path.join(os.path.dirname(__file__), ".state")
STATE_FILE = os.path.join(STATE_DIR, "enrich_calls.json")
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
        print("Usage: python3 tools/enrich.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    call_log = load_call_log()

    if len(call_log) >= BUDGET:
        print(f"ERROR: enrich budget exceeded ({BUDGET} calls max, already made {len(call_log)})", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as f:
        records = json.load(f)

    enriched = []
    timestamp = datetime.now(timezone.utc).isoformat()
    for record in records:
        result = dict(record)
        result["enriched"] = True
        result["enriched_at"] = timestamp
        enriched.append(result)

    with open(output_file, "w") as f:
        json.dump(enriched, f, indent=2)

    call_log.append({
        "call_number": len(call_log) + 1,
        "input": input_file,
        "output": output_file,
        "records_processed": len(records)
    })
    save_call_log(call_log)

    print(f"enrich: processed {len(records)} records (call {len(call_log)}/{BUDGET})")


if __name__ == "__main__":
    main()
