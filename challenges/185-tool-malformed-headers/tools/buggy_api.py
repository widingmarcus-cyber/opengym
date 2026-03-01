#!/usr/bin/env python3
"""A buggy API tool that outputs warning lines mixed with JSON data."""

import argparse
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("buggy_api")
def main():
    parser = argparse.ArgumentParser(description="Buggy API tool with mixed output")
    parser.parse_args()  # No arguments needed

    # Output warning lines mixed with the actual JSON response
    sys.stdout.write("WARNING: Deprecated endpoint\n")
    sys.stdout.write('{"data": "valid_result_88"}\n')
    sys.stdout.write("WARNING: Update your client\n")


if __name__ == "__main__":
    main()
