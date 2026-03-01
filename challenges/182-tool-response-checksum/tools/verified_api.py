#!/usr/bin/env python3
"""An API tool that returns data with a SHA-256 checksum for verification."""

import argparse
import hashlib
import json


def main():
    parser = argparse.ArgumentParser(description="Verified API tool with checksum")
    parser.parse_args()  # No arguments needed, but keep argparse for consistency

    data = "important_payload_123"
    checksum = hashlib.sha256(data.encode()).hexdigest()

    response = {
        "data": data,
        "checksum": checksum
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
