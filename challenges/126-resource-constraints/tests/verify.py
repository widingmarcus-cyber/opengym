#!/usr/bin/env python3
"""Verify Challenge 126: Resource Constraints — all items looked up within budget."""

import json
import os

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_PATH = os.path.join(CHALLENGE_DIR, "setup", "results.json")
BUDGET_PATH = os.path.join(CHALLENGE_DIR, "tools", ".state", "budget.json")

# Expected data for each item
EXPECTED = {
    "apple": {"category": "fruit", "color": "red", "calories": 95},
    "banana": {"category": "fruit", "color": "yellow", "calories": 105},
    "cherry": {"category": "fruit", "color": "red", "calories": 77},
    "date": {"category": "fruit", "color": "brown", "calories": 282},
    "elderberry": {"category": "berry", "color": "purple", "calories": 73},
    "fig": {"category": "fruit", "color": "purple", "calories": 74},
    "grape": {"category": "fruit", "color": "green", "calories": 62},
    "honeydew": {"category": "melon", "color": "green", "calories": 64},
    "kiwi": {"category": "fruit", "color": "brown", "calories": 42},
    "lemon": {"category": "citrus", "color": "yellow", "calories": 17},
}

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def main():
    # Test 1: results.json exists with all 10 items
    if not os.path.exists(RESULTS_PATH):
        check("results_exist", False, "setup/results.json not found")
        print_results()
        return

    try:
        with open(RESULTS_PATH, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        check("results_exist", False, f"Invalid JSON in results.json: {e}")
        print_results()
        return

    # Normalize: data might be a dict or a list of dicts
    if isinstance(data, list):
        # Convert list of {name: ..., ...} to dict
        merged = {}
        for item in data:
            if isinstance(item, dict):
                merged.update(item)
        data = merged

    all_items = set(EXPECTED.keys())
    found_items = set(k.lower() for k in data.keys() if k.lower() in all_items)
    check(
        "results_all_10_items",
        len(found_items) == 10,
        f"Found {len(found_items)} of 10 items: {found_items}",
    )

    # Test 2: Each item has category, color, calories
    all_have_fields = True
    for item_name in EXPECTED:
        item_data = data.get(item_name) or data.get(item_name.capitalize())
        if item_data is None:
            all_have_fields = False
            continue
        for field in ["category", "color", "calories"]:
            if field not in item_data:
                all_have_fields = False
    check(
        "items_have_all_fields",
        all_have_fields,
        "Each item should have category, color, and calories",
    )

    # Test 3: Budget not exceeded
    if os.path.exists(BUDGET_PATH):
        try:
            with open(BUDGET_PATH, "r") as f:
                budget = json.load(f)
            calls = budget.get("calls", 999)
            check(
                "budget_not_exceeded",
                calls <= 5,
                f"Used {calls} of 5 allowed calls",
            )
        except Exception as e:
            check("budget_not_exceeded", False, f"Could not read budget: {e}")
    else:
        check("budget_not_exceeded", False, "budget.json not found")

    # Test 4: Data correctness
    all_correct = True
    wrong = []
    for item_name, expected_data in EXPECTED.items():
        item_data = data.get(item_name) or data.get(item_name.capitalize())
        if item_data is None:
            all_correct = False
            wrong.append(f"{item_name}: missing")
            continue
        for field, expected_val in expected_data.items():
            actual_val = item_data.get(field)
            if str(actual_val).lower() != str(expected_val).lower():
                all_correct = False
                wrong.append(f"{item_name}.{field}: expected {expected_val}, got {actual_val}")
    check(
        "data_correct",
        all_correct,
        "All data correct" if all_correct else f"Mismatches: {wrong[:5]}",
    )

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
