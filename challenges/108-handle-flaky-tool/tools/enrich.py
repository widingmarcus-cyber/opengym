#!/usr/bin/env python3
"""Data enrichment tool -- looks up product details by SKU.

This tool is intentionally flaky: it fails on every other call using
a persistent call counter stored in tools/.state/call_count.txt.
"""

import json
import os
import sys
try:
    from _audit import audit_tool
except ImportError:
    def audit_tool(name):
        def decorator(func): return func
        return decorator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(SCRIPT_DIR, ".state")
COUNTER_FILE = os.path.join(STATE_DIR, "call_count.txt")

# Product lookup table
PRODUCTS = {
    "SKU-001": {"sku": "SKU-001", "name": "Widget Alpha", "price": 29.99, "in_stock": True},
    "SKU-002": {"sku": "SKU-002", "name": "Widget Beta", "price": 49.99, "in_stock": True},
    "SKU-003": {"sku": "SKU-003", "name": "Gadget Pro", "price": 99.99, "in_stock": False},
    "SKU-004": {"sku": "SKU-004", "name": "Gadget Lite", "price": 19.99, "in_stock": True},
    "SKU-005": {"sku": "SKU-005", "name": "Mega Bundle", "price": 149.99, "in_stock": True},
}


def get_and_increment_counter():
    """Read the call counter, increment it, and return the NEW value."""
    os.makedirs(STATE_DIR, exist_ok=True)

    count = 0
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                count = int(f.read().strip())
        except (ValueError, IOError):
            count = 0

    count += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

    return count


@audit_tool("enrich")
def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Enrich product data by SKU lookup.")
        print("Usage: python enrich.py SKU")
        print()
        print("Returns JSON with product details for the given SKU.")
        print("Supported SKUs: SKU-001 through SKU-005")
        sys.exit(0)

    if len(sys.argv) < 2:
        print("Error: No SKU provided. Use --help for usage.", file=sys.stderr)
        sys.exit(1)

    sku = sys.argv[1].strip()

    # Increment counter and check if this call should fail
    call_num = get_and_increment_counter()

    # Odd calls fail, even calls succeed
    if call_num % 2 == 1:
        print("Error: Service temporarily unavailable", file=sys.stderr)
        sys.exit(1)

    # Lookup the SKU
    if sku not in PRODUCTS:
        print(f"Error: Unknown SKU '{sku}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(PRODUCTS[sku], indent=2))


if __name__ == "__main__":
    main()
