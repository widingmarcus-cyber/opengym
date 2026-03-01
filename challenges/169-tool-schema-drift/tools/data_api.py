#!/usr/bin/env python3
"""Simulates a data API with versioned response schemas.

--version v1: Returns {"result": 42}
--version v2: Returns {"data": {"value": 42}}
Default (no version): Returns v2 format (schema has drifted)
"""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Data API with versioned schema")
    parser.add_argument("--version", choices=["v1", "v2"], default=None,
                        help="API version (v1 or v2). Defaults to latest (v2).")
    args = parser.parse_args()

    version = args.version if args.version else "v2"

    if version == "v1":
        response = {"result": 42}
    else:
        response = {"data": {"value": 42}}

    print(json.dumps(response))


if __name__ == "__main__":
    main()
