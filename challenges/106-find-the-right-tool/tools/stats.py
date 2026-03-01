#!/usr/bin/env python3
"""Compute basic statistics for a CSV file."""

import argparse
import csv
import sys
import os
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("stats")
def main():
    parser = argparse.ArgumentParser(
        description="Compute basic statistics for a CSV file (row count, column names, etc.)"
    )
    parser.add_argument("input_file", help="Path to the CSV file to analyze")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(args.input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if headers is None:
            print("Error: CSV file is empty.", file=sys.stderr)
            sys.exit(1)

        row_count = sum(1 for _ in reader)

    print(f"File: {args.input_file}")
    print(f"Columns ({len(headers)}): {', '.join(headers)}")
    print(f"Rows: {row_count}")


if __name__ == "__main__":
    main()
