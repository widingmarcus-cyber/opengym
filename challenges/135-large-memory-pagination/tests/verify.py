#!/usr/bin/env python3
"""Verification script for Challenge 135: Large Memory Pagination"""
import json
import os
import sys

CHALLENGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(CHALLENGE_DIR, "setup")
MEMORY_DIR = os.path.join(SETUP_DIR, "memory")

# Test 1: All 4 page files exist
expected_pages = ["page_1.json", "page_2.json", "page_3.json", "page_4.json"]
missing_pages = []
for page in expected_pages:
    if not os.path.exists(os.path.join(MEMORY_DIR, page)):
        missing_pages.append(page)

if not missing_pages:
    print(json.dumps({"test": "page_files_exist", "passed": True, "message": "All 4 page files exist"}))
else:
    print(json.dumps({"test": "page_files_exist", "passed": False, "message": f"Missing page files: {missing_pages}"}))
    sys.exit(0)

# Test 2: Each page file has at most 50 entries
all_pages_valid = True
page_counts = {}
all_entries = {}
for page_name in expected_pages:
    page_path = os.path.join(MEMORY_DIR, page_name)
    try:
        with open(page_path, "r") as f:
            page_data = json.load(f)
        if not isinstance(page_data, dict):
            all_pages_valid = False
            print(json.dumps({"test": "page_size_limit", "passed": False, "message": f"{page_name} is not a JSON object"}))
            break
        page_counts[page_name] = len(page_data)
        if len(page_data) > 50:
            all_pages_valid = False
            print(json.dumps({"test": "page_size_limit", "passed": False, "message": f"{page_name} has {len(page_data)} entries (max 50)"}))
            break
        all_entries.update(page_data)
    except (json.JSONDecodeError, IOError) as e:
        all_pages_valid = False
        print(json.dumps({"test": "page_size_limit", "passed": False, "message": f"Error reading {page_name}: {e}"}))
        break

if all_pages_valid:
    counts_str = ", ".join(f"{k}: {v}" for k, v in page_counts.items())
    print(json.dumps({"test": "page_size_limit", "passed": True, "message": f"All pages have <= 50 entries ({counts_str})"}))

# Test 3: Total entries across all pages = 200
total_entries = len(all_entries)
if total_entries == 200:
    print(json.dumps({"test": "total_entries", "passed": True, "message": "Total entries across all pages is 200"}))
else:
    print(json.dumps({"test": "total_entries", "passed": False, "message": f"Expected 200 total entries, found {total_entries}"}))

# Test 4: Fact 137 is correctly stored
fact_137 = all_entries.get("137", None)
expected_fact = "The speed of light is 299792458 m/s"
if fact_137 == expected_fact:
    print(json.dumps({"test": "fact_137_stored", "passed": True, "message": "Fact 137 is correctly stored in memory"}))
elif fact_137 is None:
    print(json.dumps({"test": "fact_137_stored", "passed": False, "message": "Fact 137 not found in any page file"}))
else:
    print(json.dumps({"test": "fact_137_stored", "passed": False, "message": f"Fact 137 has wrong value: '{fact_137}'"}))

# Test 5: answer.txt exists and has the correct fact text
answer_path = os.path.join(SETUP_DIR, "answer.txt")
if not os.path.exists(answer_path):
    print(json.dumps({"test": "answer_correct", "passed": False, "message": "answer.txt does not exist"}))
    sys.exit(0)

with open(answer_path, "r") as f:
    answer = f.read().strip()

if answer == expected_fact:
    print(json.dumps({"test": "answer_correct", "passed": True, "message": "answer.txt contains the correct fact text"}))
else:
    print(json.dumps({"test": "answer_correct", "passed": False, "message": f"Expected '{expected_fact}', got '{answer}'"}))
