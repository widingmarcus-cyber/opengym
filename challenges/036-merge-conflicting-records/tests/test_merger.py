"""Tests for Challenge 036: Merge Conflicting Records."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from merger import merge

DATA_A = Path(__file__).parent.parent / "setup" / "dataset_a.json"
DATA_B = Path(__file__).parent.parent / "setup" / "dataset_b.json"


def load_datasets():
    with open(DATA_A) as f:
        a = json.load(f)
    with open(DATA_B) as f:
        b = json.load(f)
    return a, b


def test_merge_returns_dict_with_keys():
    a, b = load_datasets()
    result = merge(a, b)
    assert isinstance(result, dict)
    assert "merged" in result
    assert "conflicts" in result


def test_merged_count():
    a, b = load_datasets()
    result = merge(a, b)
    assert len(result["merged"]) == 8


def test_merged_sorted_by_id():
    a, b = load_datasets()
    result = merge(a, b)
    ids = [r["id"] for r in result["merged"]]
    assert ids == ["001", "002", "003", "004", "005", "006", "007", "008"]


def test_newer_record_wins_b_newer():
    a, b = load_datasets()
    result = merge(a, b)
    merged_by_id = {r["id"]: r for r in result["merged"]}
    assert merged_by_id["001"]["email"] == "alice.j@company.com"
    assert merged_by_id["003"]["name"] == "Charles Brown"
    assert merged_by_id["003"]["department"] == "Design"


def test_newer_record_wins_a_newer():
    a, b = load_datasets()
    result = merge(a, b)
    merged_by_id = {r["id"]: r for r in result["merged"]}
    assert merged_by_id["002"]["department"] == "Marketing"


def test_unique_records_included():
    a, b = load_datasets()
    result = merge(a, b)
    merged_by_id = {r["id"]: r for r in result["merged"]}
    assert merged_by_id["004"]["name"] == "Diana Prince"
    assert merged_by_id["005"]["name"] == "Eve Torres"
    assert merged_by_id["006"]["name"] == "Frank Castle"
    assert merged_by_id["007"]["name"] == "Grace Hopper"


def test_conflicts_count():
    a, b = load_datasets()
    result = merge(a, b)
    assert len(result["conflicts"]) == 5


def test_conflicts_content():
    a, b = load_datasets()
    result = merge(a, b)
    conflicts = result["conflicts"]
    conflict_tuples = {(c["key"], c["field"]) for c in conflicts}
    assert ("001", "email") in conflict_tuples
    assert ("002", "department") in conflict_tuples
    assert ("003", "name") in conflict_tuples
    assert ("003", "department") in conflict_tuples
    assert ("008", "email") in conflict_tuples


def test_conflict_values():
    a, b = load_datasets()
    result = merge(a, b)
    conflicts = result["conflicts"]
    email_conflict = [c for c in conflicts if c["key"] == "001" and c["field"] == "email"][0]
    assert email_conflict["value_a"] == "alice@company.com"
    assert email_conflict["value_b"] == "alice.j@company.com"


def test_custom_key_field():
    records_a = [
        {"code": "X1", "value": 10, "updated_at": "2024-01-01T00:00:00"},
        {"code": "X2", "value": 20, "updated_at": "2024-01-01T00:00:00"},
    ]
    records_b = [
        {"code": "X1", "value": 15, "updated_at": "2024-06-01T00:00:00"},
        {"code": "X3", "value": 30, "updated_at": "2024-01-01T00:00:00"},
    ]
    result = merge(records_a, records_b, key="code")
    assert len(result["merged"]) == 3
    merged_by_code = {r["code"]: r for r in result["merged"]}
    assert merged_by_code["X1"]["value"] == 15
