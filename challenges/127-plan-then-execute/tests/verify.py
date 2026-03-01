#!/usr/bin/env python3
"""Verify Challenge 127: Plan Then Execute — plan exists and inventory module works."""

import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
PLAN_PATH = os.path.join(SETUP_DIR, "plan.md")

sys.path.insert(0, SETUP_DIR)

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def main():
    # Test 1: plan.md exists and has >100 characters
    if os.path.exists(PLAN_PATH):
        with open(PLAN_PATH, "r") as f:
            plan_content = f.read()
        check(
            "plan_exists_and_substantive",
            len(plan_content) > 100,
            f"plan.md has {len(plan_content)} characters (need >100)",
        )
    else:
        plan_content = ""
        check("plan_exists_and_substantive", False, "plan.md not found")

    # Test 2: plan mentions key functions
    key_terms = ["add_item", "remove_item", "get_item", "total_value", "low_stock"]
    plan_lower = plan_content.lower()
    mentioned = [t for t in key_terms if t in plan_lower]
    check(
        "plan_mentions_functions",
        len(mentioned) >= 3,
        f"Plan mentions {len(mentioned)}/5 key functions: {mentioned}",
    )

    # Tests 3-8: Import and test the inventory module
    try:
        from inventory import Inventory

        inv = Inventory()

        # Test 3: add_item works
        try:
            inv.add_item("Widget", 10, 5.99)
            check("add_item_works", True, "add_item('Widget', 10, 5.99) succeeded")
        except Exception as e:
            check("add_item_works", False, f"add_item failed: {e}")

        # Test 4: get_item returns correct data
        try:
            item = inv.get_item("Widget")
            has_qty = False
            has_price = False
            if isinstance(item, dict):
                has_qty = item.get("quantity", item.get("qty")) == 10
                has_price = item.get("price") == 5.99
            check(
                "get_item_works",
                item is not None and has_qty and has_price,
                f"get_item('Widget') returned: {item}",
            )
        except Exception as e:
            check("get_item_works", False, f"get_item failed: {e}")

        # Test 5: remove_item reduces quantity
        try:
            inv.remove_item("Widget", 3)
            item_after = inv.get_item("Widget")
            remaining = None
            if isinstance(item_after, dict):
                remaining = item_after.get("quantity", item_after.get("qty"))
            check(
                "remove_item_works",
                remaining == 7,
                f"After removing 3 from 10, quantity is {remaining} (expected 7)",
            )
        except Exception as e:
            check("remove_item_works", False, f"remove_item failed: {e}")

        # Test 6: remove_item with too many raises error
        try:
            inv.remove_item("Widget", 100)
            check(
                "remove_insufficient_raises",
                False,
                "Expected error when removing more than available",
            )
        except (ValueError, Exception):
            check(
                "remove_insufficient_raises",
                True,
                "Error raised for insufficient quantity",
            )

        # Test 7: total_value is correct
        try:
            # Widget: 7 * 5.99 = 41.93
            inv.add_item("Gadget", 5, 10.00)
            # Gadget: 5 * 10.00 = 50.00
            # Total: 41.93 + 50.00 = 91.93
            total = inv.total_value()
            expected = 7 * 5.99 + 5 * 10.00
            check(
                "total_value_correct",
                abs(float(total) - expected) < 0.01,
                f"total_value() = {total}, expected {expected}",
            )
        except Exception as e:
            check("total_value_correct", False, f"total_value failed: {e}")

        # Test 8: low_stock returns correct items
        try:
            # Widget: 7, Gadget: 5
            low = inv.low_stock(6)
            # Only Gadget (5) is below threshold 6
            is_list = isinstance(low, list)
            if is_list:
                low_names = []
                for item in low:
                    if isinstance(item, dict):
                        low_names.append(item.get("name", ""))
                    elif isinstance(item, str):
                        low_names.append(item)
                    elif isinstance(item, tuple) and len(item) > 0:
                        low_names.append(item[0])
                has_gadget = "Gadget" in low_names
                no_widget = "Widget" not in low_names
                check(
                    "low_stock_correct",
                    has_gadget and no_widget,
                    f"low_stock(6) returned names: {low_names}",
                )
            else:
                check("low_stock_correct", False, f"low_stock returned non-list: {low}")
        except Exception as e:
            check("low_stock_correct", False, f"low_stock failed: {e}")

    except ImportError as e:
        for name in [
            "add_item_works", "get_item_works", "remove_item_works",
            "remove_insufficient_raises", "total_value_correct", "low_stock_correct",
        ]:
            check(name, False, f"Could not import Inventory: {e}")

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
