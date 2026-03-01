#!/usr/bin/env python3
"""Compress a file using gzip."""

import argparse
import gzip
import sys
import os
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("compress")
def main():
    parser = argparse.ArgumentParser(description="Compress a file using gzip")
    parser.add_argument("input_file", help="Path to the file to compress")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: input_file.gz)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    output_path = args.output or args.input_file + ".gz"

    with open(args.input_file, "rb") as f_in:
        with gzip.open(output_path, "wb") as f_out:
            f_out.write(f_in.read())

    print(f"Compressed '{args.input_file}' -> '{output_path}'")


if __name__ == "__main__":
    main()
