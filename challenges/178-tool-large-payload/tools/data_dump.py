#!/usr/bin/env python3
"""A data dump tool that returns paginated records."""

import argparse
import json
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("data_dump")
def main():
    parser = argparse.ArgumentParser(description="Paginated data dump tool")
    parser.add_argument("--page", required=True, type=int, help="Page number (1-based)")
    args = parser.parse_args()

    page = args.page

    if page == 1:
        # Records 1-50, value = id * 2
        records = [{"id": i, "value": i * 2} for i in range(1, 51)]
        response = {
            "data": records,
            "page": 1,
            "has_more": True,
            "total_pages": 2
        }
    elif page == 2:
        # Records 51-100, value = id * 2
        records = [{"id": i, "value": i * 2} for i in range(51, 101)]
        response = {
            "data": records,
            "page": 2,
            "has_more": False,
            "total_pages": 2
        }
    else:
        # No more data
        response = {
            "data": [],
            "page": page,
            "has_more": False,
            "total_pages": 2
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
