"""Tests for Challenge 034: Normalize Messy Data."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from normalizer import normalize_records

DATA_FILE = Path(__file__).parent.parent / "setup" / "messy_data.json"


def load_records():
    with open(DATA_FILE) as f:
        return json.load(f)


def test_returns_list_of_dicts():
    records = load_records()
    result = normalize_records(records)
    assert isinstance(result, list)
    assert all(isinstance(r, dict) for r in result)


def test_removes_duplicates():
    records = load_records()
    result = normalize_records(records)
    assert len(result) == 14


def test_iso_date_passthrough():
    records = [{"name": "Alice", "date": "2024-01-15", "status": "Active", "email": "a@b.com"}]
    result = normalize_records(records)
    assert result[0]["date"] == "2024-01-15"


def test_named_month_date_format():
    records = [{"name": "Bob", "date": "Jan 20, 2024", "status": "Active", "email": "b@b.com"}]
    result = normalize_records(records)
    assert result[0]["date"] == "2024-01-20"


def test_ddmmyyyy_date_format():
    records = [{"name": "Charlie", "date": "05/02/2024", "status": "Active", "email": "c@b.com"}]
    result = normalize_records(records)
    assert result[0]["date"] == "2024-02-05"


def test_status_lowercased():
    records = load_records()
    result = normalize_records(records)
    statuses = {r["status"] for r in result}
    assert statuses == {"active", "inactive"}


def test_names_stripped():
    records = load_records()
    result = normalize_records(records)
    for r in result:
        assert r["name"] == r["name"].strip()
    names = [r["name"] for r in result]
    assert "Bob Smith" in names
    assert "Charlie Brown" in names
    assert "Hank Pym" in names


def test_preserves_order_first_occurrence():
    records = load_records()
    result = normalize_records(records)
    names = [r["name"] for r in result]
    assert names[0] == "Alice Johnson"
    assert names[1] == "Bob Smith"
    assert names[2] == "Charlie Brown"
    assert names[6] == "Grace Hopper"
