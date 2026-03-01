#!/usr/bin/env python3
"""A text API tool that returns text in different encodings."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Text API tool with encoding support")
    parser.add_argument("--encoding", default="utf-8", help="Encoding to return text in (default: utf-8)")
    args = parser.parse_args()

    if args.encoding.lower() in ("utf-8", "utf8"):
        response = {
            "text": "caf\u00e9",
            "encoding": "utf-8"
        }
        print(json.dumps(response, ensure_ascii=False))
    elif args.encoding.lower() in ("latin1", "latin-1", "iso-8859-1"):
        response = {
            "text": "caf\\xe9",
            "encoding": "latin1"
        }
        print(json.dumps(response))
    else:
        print(json.dumps({"error": f"Unsupported encoding: {args.encoding}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
