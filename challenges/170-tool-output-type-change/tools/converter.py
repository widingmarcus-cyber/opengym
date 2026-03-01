#!/usr/bin/env python3
"""Simulates a value converter that returns different types based on format.

--format json: Returns the value as a string: {"output": "42"}
--format number: Returns the value as an integer: {"output": 42}
"""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Value converter simulator")
    parser.add_argument("--input", required=True, help="Input value to convert")
    parser.add_argument("--format", choices=["json", "number"], default="json",
                        help="Output format (json returns string, number returns int)")
    args = parser.parse_args()

    if args.format == "json":
        response = {"output": str(args.input)}
    elif args.format == "number":
        try:
            response = {"output": int(args.input)}
        except ValueError:
            try:
                response = {"output": float(args.input)}
            except ValueError:
                response = {"error": f"Cannot convert '{args.input}' to number"}
    else:
        response = {"error": f"Unknown format: {args.format}"}

    print(json.dumps(response))


if __name__ == "__main__":
    main()
