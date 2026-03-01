#!/usr/bin/env python3
"""An API tool that returns cached data by default. Use --no-cache for fresh data."""

import argparse
import json
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("cached_api")
def main():
    parser = argparse.ArgumentParser(description="Cached API tool")
    parser.add_argument("--key", required=True, help="Data key to look up")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache and get fresh data")
    args = parser.parse_args()

    if args.no_cache:
        response = {
            "data": "fresh_value",
            "cached": False,
            "key": args.key
        }
    else:
        response = {
            "data": "old_value",
            "cached": True,
            "cache_age_seconds": 3600,
            "key": args.key
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
