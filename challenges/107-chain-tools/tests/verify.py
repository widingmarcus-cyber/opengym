#!/usr/bin/env python3
"""Verify Challenge 107: Chain Tools."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_FILE = os.path.join(CHALLENGE_DIR, "setup", "report.json")


def check(test_name, passed, message):
    print(json.dumps({"test": test_name, "passed": passed, "message": message}))
    return passed


def main():
    all_passed = True

    # Test 1: report.json exists
    if not os.path.exists(REPORT_FILE):
        check("report_exists", False, f"setup/report.json not found at {REPORT_FILE}")
        check("valid_json", False, "Skipped: report file missing")
        check("widget_aggregation", False, "Skipped: report file missing")
        check("gadget_aggregation", False, "Skipped: report file missing")
        check("has_metadata", False, "Skipped: report file missing")
        sys.exit(0)

    all_passed &= check("report_exists", True, "setup/report.json exists")

    # Test 2: valid JSON
    try:
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            report = json.load(f)
        all_passed &= check("valid_json", True, "report.json contains valid JSON")
    except (json.JSONDecodeError, Exception) as e:
        check("valid_json", False, f"report.json is not valid JSON: {e}")
        check("widget_aggregation", False, "Skipped: invalid JSON")
        check("gadget_aggregation", False, "Skipped: invalid JSON")
        check("has_metadata", False, "Skipped: invalid JSON")
        sys.exit(0)

    # Find the data array — support both wrapped and flat formats
    data = None
    metadata = None
    if isinstance(report, dict):
        data = report.get("data", None)
        metadata = report.get("metadata", None)
    elif isinstance(report, list):
        data = report

    if data is None:
        check("widget_aggregation", False, "Could not find data array in report")
        check("gadget_aggregation", False, "Skipped")
        check("has_metadata", False, "Skipped")
        sys.exit(0)

    # Build lookup by product
    by_product = {}
    for record in data:
        product = record.get("product", "")
        by_product[product] = record

    # Test 3: Widget aggregation
    # Widget: SALE 3 + SALE 2 - RETURN 1 = net 4, revenue = 4 * 29.99 = 119.96
    widget = by_product.get("Widget")
    if widget is None:
        all_passed &= check("widget_aggregation", False, "No Widget record found in data")
    else:
        net_qty = widget.get("net_quantity", widget.get("quantity", None))
        revenue = widget.get("total_revenue", widget.get("revenue", None))

        errors = []
        if net_qty is None:
            errors.append("Missing net_quantity field")
        elif net_qty != 4:
            errors.append(f"net_quantity: expected 4, got {net_qty}")

        if revenue is None:
            errors.append("Missing total_revenue field")
        elif abs(float(revenue) - 119.96) > 0.02:
            errors.append(f"total_revenue: expected ~119.96, got {revenue}")

        if errors:
            all_passed &= check("widget_aggregation", False, "; ".join(errors))
        else:
            all_passed &= check(
                "widget_aggregation", True, "Widget: net_quantity=4, total_revenue=119.96"
            )

    # Test 4: Gadget aggregation
    # Gadget: SALE 1 + SALE 2 = net 3, revenue = 3 * 49.99 = 149.97
    gadget = by_product.get("Gadget")
    if gadget is None:
        all_passed &= check("gadget_aggregation", False, "No Gadget record found in data")
    else:
        net_qty = gadget.get("net_quantity", gadget.get("quantity", None))
        revenue = gadget.get("total_revenue", gadget.get("revenue", None))

        errors = []
        if net_qty is None:
            errors.append("Missing net_quantity field")
        elif net_qty != 3:
            errors.append(f"net_quantity: expected 3, got {net_qty}")

        if revenue is None:
            errors.append("Missing total_revenue field")
        elif abs(float(revenue) - 149.97) > 0.02:
            errors.append(f"total_revenue: expected ~149.97, got {revenue}")

        if errors:
            all_passed &= check("gadget_aggregation", False, "; ".join(errors))
        else:
            all_passed &= check(
                "gadget_aggregation", True, "Gadget: net_quantity=3, total_revenue=149.97"
            )

    # Test 5: metadata present with record_count
    if metadata is None:
        all_passed &= check(
            "has_metadata", False, "No metadata object found in report"
        )
    else:
        rc = metadata.get("record_count", None)
        if rc is None:
            all_passed &= check(
                "has_metadata", False, "metadata missing record_count field"
            )
        elif rc == 2:
            all_passed &= check(
                "has_metadata", True, "metadata.record_count = 2 (Widget + Gadget)"
            )
        else:
            all_passed &= check(
                "has_metadata",
                True,
                f"metadata.record_count present (got {rc})",
            )


if __name__ == "__main__":
    main()
