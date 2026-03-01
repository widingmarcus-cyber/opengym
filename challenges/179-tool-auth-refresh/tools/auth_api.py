#!/usr/bin/env python3
"""An API tool that requires authentication. Supports token refresh."""

import argparse
import json
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator


@audit_tool("auth_api")
def main():
    parser = argparse.ArgumentParser(description="Authenticated API tool")
    parser.add_argument("--token", help="Authentication token")
    parser.add_argument("--refresh", action="store_true", help="Refresh the authentication token")
    args = parser.parse_args()

    if args.refresh:
        response = {
            "status": 200,
            "new_token": "fresh_token_xyz"
        }
        print(json.dumps(response))
        return

    if not args.token:
        print(json.dumps({"status": 400, "error": "Token required. Use --token <token> or --refresh."}))
        sys.exit(1)

    if args.token == "expired_token":
        response = {
            "status": 401,
            "error": "Token expired"
        }
    elif args.token == "fresh_token_xyz":
        response = {
            "status": 200,
            "data": "secret_data_99"
        }
    else:
        response = {
            "status": 403,
            "error": "Invalid token"
        }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
