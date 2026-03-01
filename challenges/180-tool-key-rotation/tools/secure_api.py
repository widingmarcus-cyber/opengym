#!/usr/bin/env python3
"""A secure API tool that requires a valid API key. Handles key rotation."""

import argparse
import json
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("secure_api")
def main():
    parser = argparse.ArgumentParser(description="Secure API tool with key rotation")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    args = parser.parse_args()

    if args.api_key == "key_v1":
        response = {
            "status": 403,
            "error": "API key rotated. Use updated key."
        }
    elif args.api_key == "key_v2":
        response = {
            "status": 200,
            "data": "classified_info_55"
        }
    else:
        response = {
            "status": 403,
            "error": "Invalid API key."
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
