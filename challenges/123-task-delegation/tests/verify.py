#!/usr/bin/env python3
"""Verify Challenge 123: Task Delegation — manager created tasks, worker implemented them."""

import json
import os
import sys
import glob as globmod

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
TASKS_DIR = os.path.join(SETUP_DIR, "tasks")

# Add setup dir to path so we can import contact_book
sys.path.insert(0, SETUP_DIR)

results = []


def check(name, passed, message=""):
    results.append({"test": name, "passed": passed, "message": message})


def main():
    # Test 1: At least 2 task files exist in setup/tasks/
    task_files = [
        f for f in globmod.glob(os.path.join(TASKS_DIR, "task_*.md"))
    ]
    check(
        "task_files_exist",
        len(task_files) >= 2,
        f"Found {len(task_files)} task files (need >= 2)",
    )

    # Test 2-7: Import and test the contact book
    try:
        from contact_book import ContactBook

        book = ContactBook()

        # Test 2: Can create instance
        check("create_instance", True, "ContactBook instance created")

        # Test 3: add_contact works
        try:
            book.add_contact("Alice", "555-0001", "alice@example.com")
            check("add_contact", True, "add_contact executed without error")
        except Exception as e:
            check("add_contact", False, f"add_contact failed: {e}")

        # Test 4: search_contact finds the contact
        try:
            result = book.search_contact("Alice")
            # Accept various return formats: dict, object, list, etc.
            found = False
            if result is not None:
                if isinstance(result, dict):
                    found = result.get("name") == "Alice" or "Alice" in str(result)
                elif isinstance(result, (list, tuple)):
                    found = len(result) > 0
                else:
                    found = "Alice" in str(result)
            check(
                "search_contact",
                found,
                f"search_contact('Alice') returned: {result}",
            )
        except Exception as e:
            check("search_contact", False, f"search_contact failed: {e}")

        # Test 5: list_contacts returns added contacts
        try:
            all_contacts = book.list_contacts()
            has_contacts = all_contacts is not None and len(all_contacts) > 0
            check(
                "list_contacts",
                has_contacts,
                f"list_contacts returned {len(all_contacts) if all_contacts else 0} contacts",
            )
        except Exception as e:
            check("list_contacts", False, f"list_contacts failed: {e}")

        # Test 6: remove_contact works
        try:
            book.remove_contact("Alice")
            check("remove_contact", True, "remove_contact executed without error")
        except Exception as e:
            check("remove_contact", False, f"remove_contact failed: {e}")

        # Test 7: search after remove returns None or empty
        try:
            result_after = book.search_contact("Alice")
            is_empty = (
                result_after is None
                or result_after == []
                or result_after == {}
                or result_after == ""
            )
            check(
                "search_after_remove",
                is_empty,
                f"search after remove returned: {result_after}",
            )
        except Exception as e:
            check("search_after_remove", False, f"search after remove failed: {e}")

    except ImportError as e:
        check("create_instance", False, f"Could not import ContactBook: {e}")
        check("add_contact", False, "Could not import ContactBook")
        check("search_contact", False, "Could not import ContactBook")
        check("list_contacts", False, "Could not import ContactBook")
        check("remove_contact", False, "Could not import ContactBook")
        check("search_after_remove", False, "Could not import ContactBook")
    except Exception as e:
        check("create_instance", False, f"Unexpected error creating ContactBook: {e}")

    print_results()


def print_results():
    for r in results:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
