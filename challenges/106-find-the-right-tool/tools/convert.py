#!/usr/bin/env python3
"""Convert CSV files to other formats (JSON, YAML, XML)."""

import argparse
import csv
import json
import sys
import os
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


def csv_to_json(filepath):
    """Convert CSV file to JSON array."""
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric-looking fields
            converted = {}
            for key, value in row.items():
                try:
                    converted[key] = int(value)
                except (ValueError, TypeError):
                    try:
                        converted[key] = float(value)
                    except (ValueError, TypeError):
                        converted[key] = value
            records.append(converted)
    return json.dumps(records, indent=2, ensure_ascii=False)


def csv_to_yaml(filepath):
    """Convert CSV file to YAML format."""
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    lines = []
    for record in records:
        lines.append("-")
        for key, value in record.items():
            lines.append(f"  {key}: {value}")
    return "\n".join(lines)


def csv_to_xml(filepath):
    """Convert CSV file to XML format."""
    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<records>"]
    for record in records:
        lines.append("  <record>")
        for key, value in record.items():
            lines.append(f"    <{key}>{value}</{key}>")
        lines.append("  </record>")
    lines.append("</records>")
    return "\n".join(lines)


@audit_tool("convert")
def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV files to JSON, YAML, or XML format"
    )
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument(
        "--format",
        required=True,
        choices=["json", "yaml", "xml"],
        help="Output format: json, yaml, or xml",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    converters = {
        "json": csv_to_json,
        "yaml": csv_to_yaml,
        "xml": csv_to_xml,
    }

    # Ensure stdout uses UTF-8 encoding for non-ASCII characters
    sys.stdout.reconfigure(encoding="utf-8")

    result = converters[args.format](args.input)
    print(result)


if __name__ == "__main__":
    main()
