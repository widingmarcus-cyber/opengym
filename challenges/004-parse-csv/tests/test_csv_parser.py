"""Tests for Challenge 004: Parse CSV."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from csv_parser import parse_csv, get_column, filter_records, average_column

DATA_FILE = str(Path(__file__).parent.parent / "setup" / "data.csv")


def test_parse_csv_returns_list():
    records = parse_csv(DATA_FILE)
    assert isinstance(records, list)
    assert len(records) == 8


def test_parse_csv_dict_keys():
    records = parse_csv(DATA_FILE)
    assert set(records[0].keys()) == {"name", "department", "salary", "years"}


def test_parse_csv_first_record():
    records = parse_csv(DATA_FILE)
    assert records[0]["name"] == "Alice"
    assert records[0]["department"] == "Engineering"


def test_get_column():
    records = parse_csv(DATA_FILE)
    names = get_column(records, "name")
    assert names == ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"]


def test_get_column_missing():
    records = parse_csv(DATA_FILE)
    try:
        get_column(records, "nonexistent")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_filter_records():
    records = parse_csv(DATA_FILE)
    eng = filter_records(records, "department", "Engineering")
    assert len(eng) == 4
    assert all(r["department"] == "Engineering" for r in eng)


def test_filter_records_no_match():
    records = parse_csv(DATA_FILE)
    result = filter_records(records, "department", "HR")
    assert result == []


def test_average_column():
    records = parse_csv(DATA_FILE)
    avg_salary = average_column(records, "salary")
    assert isinstance(avg_salary, float)
    expected = (95000 + 72000 + 105000 + 68000 + 88000 + 76000 + 82000 + 92000) / 8
    assert abs(avg_salary - expected) < 0.01
