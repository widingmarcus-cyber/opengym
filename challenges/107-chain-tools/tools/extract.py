#!/usr/bin/env python3
"""Extract records from a pipe-delimited file into JSON."""

import json
import sys
import os
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("extract")
def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Extract records from pipe-delimited file.")
        print("Usage: python extract.py INPUT_FILE")
        print()
        print("Reads a pipe-delimited text file and outputs a JSON array to stdout.")
        print("Each line should have format: date|type|product|quantity|unit_price")
        print()
        print("Output JSON fields: date, type, product, quantity (int), unit_price (float)")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Error: No input file specified. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    records = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 5:
                print(
                    f"Warning: Line {line_num} has {len(parts)} fields, expected 5. Skipping.",
                    file=sys.stderr,
                )
                continue
            record = {
                "date": parts[0],
                "type": parts[1],
                "product": parts[2],
                "quantity": int(parts[3]),
                "unit_price": float(parts[4]),
            }
            records.append(record)

    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
