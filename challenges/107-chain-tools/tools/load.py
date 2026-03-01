#!/usr/bin/env python3
"""Load processed data to a file with metadata."""

import json
import sys
from datetime import datetime, timezone
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("load")
def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Load processed data to file.")
        print("Usage: python load.py OUTPUT_FILE")
        print()
        print("Reads JSON from stdin (array of records), wraps it with metadata")
        print("(generated_at timestamp, record_count), and writes to OUTPUT_FILE.")
        print()
        print("Example: cat processed.json | python load.py report.json")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Error: No output file specified. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    output_file = sys.argv[1]

    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: Expected a JSON array from stdin.", file=sys.stderr)
        sys.exit(1)

    report = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "record_count": len(data),
        },
        "data": data,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Report written to '{output_file}' with {len(data)} records.")


if __name__ == "__main__":
    main()
