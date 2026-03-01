#!/usr/bin/env python3
"""Simulates a primary service that is permanently unavailable.

Always returns an unavailable status to simulate maintenance downtime.
"""

import argparse
import json
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("primary")
def main():
    parser = argparse.ArgumentParser(description="Primary service (currently unavailable)")
    parser.add_argument("--endpoint", default="/data", help="Service endpoint")
    parser.parse_args()

    response = {
        "status": "unavailable",
        "error": "Service is down for maintenance"
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
