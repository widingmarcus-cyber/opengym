#!/usr/bin/env python3
"""Transform records by aggregating per product."""

import json
import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print("Transform records by aggregating per product.")
        print("Reads JSON from stdin (array of records with fields:")
        print("  date, type, product, quantity, unit_price)")
        print()
        print("Outputs JSON to stdout with per-product aggregation:")
        print("  product, total_sold, total_returned, net_quantity, total_revenue")
        print()
        print("Revenue is calculated as: (sold_quantity - returned_quantity) * unit_price")
        print("Usage: cat data.json | python transform.py")
        sys.exit(0)

    try:
        raw = sys.stdin.read()
        records = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(records, list):
        print("Error: Expected a JSON array.", file=sys.stderr)
        sys.exit(1)

    # Aggregate by product
    products = {}
    for record in records:
        product = record["product"]
        quantity = record["quantity"]
        unit_price = record["unit_price"]
        record_type = record["type"]

        if product not in products:
            products[product] = {
                "product": product,
                "total_sold": 0,
                "total_returned": 0,
                "net_quantity": 0,
                "total_revenue": 0.0,
                "unit_price": unit_price,
            }

        if record_type == "SALE":
            products[product]["total_sold"] += quantity
            products[product]["net_quantity"] += quantity
            products[product]["total_revenue"] += quantity * unit_price
        elif record_type == "RETURN":
            products[product]["total_returned"] += quantity
            products[product]["net_quantity"] -= quantity
            products[product]["total_revenue"] -= quantity * unit_price

    # Remove the helper unit_price field
    result = []
    for p in products.values():
        del p["unit_price"]
        p["total_revenue"] = round(p["total_revenue"], 2)
        result.append(p)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
