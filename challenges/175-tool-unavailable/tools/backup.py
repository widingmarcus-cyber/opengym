#!/usr/bin/env python3
"""Simulates a backup service that is always available.

Returns a successful response with backup data.
"""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Backup service (always available)")
    parser.add_argument("--endpoint", default="/data", help="Service endpoint")
    parser.parse_args()

    response = {
        "status": "ok",
        "data": "backup_result_77"
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
