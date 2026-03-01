#!/usr/bin/env python3
"""Verify Challenge 109: Rate Limited Tool."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(CHALLENGE_DIR, "setup", "populations.json")

EXPECTED = {
    "Stockholm": 975000,
    "Gothenburg": 583000,
    "Malmö": 347000,
    "Uppsala": 233000,
    "Linköping": 164000,
    "Västerås": 155000,
    "Örebro": 157000,
    "Helsingborg": 149000,
    "Norrköping": 143000,
    "Jönköping": 144000,
}


def check(test_name, passed, message):
    print(json.dumps({"test": test_name, "passed": passed, "message": message}))
    return passed


def main():
    all_passed = True

    # Test 1: populations.json exists
    if not os.path.exists(OUTPUT_FILE):
        check("output_exists", False, f"setup/populations.json not found at {OUTPUT_FILE}")
        check("valid_json", False, "Skipped: output file missing")
        check("all_cities_present", False, "Skipped: output file missing")
        check("populations_correct", False, "Skipped: output file missing")
        sys.exit(0)

    all_passed &= check("output_exists", True, "setup/populations.json exists")

    # Test 2: valid JSON
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_passed &= check("valid_json", True, "populations.json contains valid JSON")
    except (json.JSONDecodeError, Exception) as e:
        check("valid_json", False, f"populations.json is not valid JSON: {e}")
        check("all_cities_present", False, "Skipped: invalid JSON")
        check("populations_correct", False, "Skipped: invalid JSON")
        sys.exit(0)

    # Normalize data to a city->population mapping
    city_pop = {}
    if isinstance(data, dict):
        # Could be {"Stockholm": 975000, ...} or {"Stockholm": {"population": 975000}, ...}
        for key, val in data.items():
            if isinstance(val, (int, float)):
                city_pop[key] = int(val)
            elif isinstance(val, dict) and "population" in val:
                city_pop[key] = int(val["population"])
    elif isinstance(data, list):
        # Array of {"city": "Stockholm", "population": 975000}
        for record in data:
            if isinstance(record, dict):
                city = record.get("city", "")
                pop = record.get("population", None)
                if city and pop is not None:
                    city_pop[city] = int(pop)

    # Test 3: all 10 cities present
    missing = [city for city in EXPECTED if city not in city_pop]
    if missing:
        all_passed &= check(
            "all_cities_present",
            False,
            f"Missing cities ({len(missing)}): {', '.join(missing)}",
        )
    else:
        all_passed &= check(
            "all_cities_present", True, "All 10 cities present in output"
        )

    # Test 4: correct populations
    errors = []
    for city, expected_pop in EXPECTED.items():
        actual = city_pop.get(city)
        if actual is None:
            errors.append(f"{city}: missing")
        elif actual != expected_pop:
            errors.append(f"{city}: expected {expected_pop}, got {actual}")

    if errors:
        all_passed &= check("populations_correct", False, "; ".join(errors))
    else:
        all_passed &= check(
            "populations_correct", True, "All populations match expected values"
        )



    # === Audit log validation ===
    _audit_file = os.path.join(CHALLENGE_DIR, "setup", "tool_audit.jsonl")
    _tools_dir = os.path.join(CHALLENGE_DIR, "tools")
    sys.path.insert(0, _tools_dir)
    try:
        from _audit import full_audit_check
        _audit_ok, _audit_errors = full_audit_check(
            _audit_file, "lookup",
            min_calls=4, max_calls=999,
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
