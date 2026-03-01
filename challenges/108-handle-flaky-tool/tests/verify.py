#!/usr/bin/env python3
"""Verify Challenge 108: Handle Flaky Tool."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(CHALLENGE_DIR, "setup", "enriched.json")

EXPECTED = {
    "SKU-001": {"name": "Widget Alpha", "price": 29.99, "in_stock": True},
    "SKU-002": {"name": "Widget Beta", "price": 49.99, "in_stock": True},
    "SKU-003": {"name": "Gadget Pro", "price": 99.99, "in_stock": False},
    "SKU-004": {"name": "Gadget Lite", "price": 19.99, "in_stock": True},
    "SKU-005": {"name": "Mega Bundle", "price": 149.99, "in_stock": True},
}


def check(test_name, passed, message):
    print(json.dumps({"test": test_name, "passed": passed, "message": message}))
    return passed


def main():
    all_passed = True

    # Test 1: enriched.json exists
    if not os.path.exists(OUTPUT_FILE):
        check("output_exists", False, f"setup/enriched.json not found at {OUTPUT_FILE}")
        check("valid_json", False, "Skipped: output file missing")
        check("all_skus_present", False, "Skipped: output file missing")
        check("data_correct", False, "Skipped: output file missing")
        sys.exit(0)

    all_passed &= check("output_exists", True, "setup/enriched.json exists")

    # Test 2: valid JSON
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_passed &= check("valid_json", True, "enriched.json contains valid JSON")
    except (json.JSONDecodeError, Exception) as e:
        check("valid_json", False, f"enriched.json is not valid JSON: {e}")
        check("all_skus_present", False, "Skipped: invalid JSON")
        check("data_correct", False, "Skipped: invalid JSON")
        sys.exit(0)

    # Normalize: accept both array and dict formats
    records = []
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # Could be {sku: {...}, ...} or a single record
        if "sku" in data:
            records = [data]
        else:
            records = list(data.values())

    # Build lookup by SKU
    by_sku = {}
    for record in records:
        if isinstance(record, dict):
            sku = record.get("sku", "")
            by_sku[sku] = record

    # Test 3: all 5 SKUs present
    missing = [sku for sku in EXPECTED if sku not in by_sku]
    if missing:
        all_passed &= check(
            "all_skus_present",
            False,
            f"Missing SKUs: {', '.join(missing)}",
        )
    else:
        all_passed &= check(
            "all_skus_present", True, "All 5 SKUs present in output"
        )

    # Test 4: data correctness
    errors = []
    for sku, expected in EXPECTED.items():
        record = by_sku.get(sku)
        if record is None:
            errors.append(f"{sku}: missing entirely")
            continue

        name = record.get("name", "")
        if name != expected["name"]:
            errors.append(f"{sku}: name expected '{expected['name']}', got '{name}'")

        price = record.get("price", None)
        if price is None:
            errors.append(f"{sku}: missing price field")
        elif abs(float(price) - expected["price"]) > 0.01:
            errors.append(
                f"{sku}: price expected {expected['price']}, got {price}"
            )

        in_stock = record.get("in_stock", None)
        if in_stock is None:
            errors.append(f"{sku}: missing in_stock field")
        elif bool(in_stock) != expected["in_stock"]:
            errors.append(
                f"{sku}: in_stock expected {expected['in_stock']}, got {in_stock}"
            )

    if errors:
        all_passed &= check("data_correct", False, "; ".join(errors))
    else:
        all_passed &= check(
            "data_correct", True, "All SKU data matches expected values"
        )



    # === Audit log validation ===
    _audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
    _tools_dir = os.path.join(CHALLENGE_DIR, "tools")
    sys.path.insert(0, _tools_dir)
    try:
        from _audit import full_audit_check
        _audit_ok, _audit_errors = full_audit_check(
            _audit_file, "enrich",
            min_calls=5, max_calls=999,
            min_gap_ms=0,
        )
        if _audit_ok:
            check("audit_log_valid", True, "Audit log signatures, sequences, and nonces valid")
        else:
            for _err in _audit_errors[:3]:
                check("audit_log_valid", False, _err)
    except ImportError:
        check("audit_log_valid", True, "Audit module not available (skipped)")
if __name__ == "__main__":
    main()
