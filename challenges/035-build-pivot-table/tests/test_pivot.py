"""Tests for Challenge 035: Build Pivot Table."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from pivot import pivot, pivot_to_table

DATA_FILE = Path(__file__).parent.parent / "setup" / "sales_data.json"


def load_records():
    with open(DATA_FILE) as f:
        return json.load(f)


def test_pivot_sum_returns_nested_dict():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "sum")
    assert isinstance(result, dict)
    assert isinstance(result["North"], dict)


def test_pivot_sum_region_by_category():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "sum")
    assert abs(result["North"]["Electronics"] - 2550.0) < 0.01
    assert abs(result["East"]["Clothing"] - 1120.0) < 0.01
    assert abs(result["West"]["Food"] - 640.0) < 0.01


def test_pivot_sum_all_regions():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "sum")
    assert abs(result["South"]["Electronics"] - 2030.0) < 0.01
    assert abs(result["South"]["Clothing"] - 1220.0) < 0.01
    assert abs(result["South"]["Food"] - 800.0) < 0.01


def test_pivot_count():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "count")
    assert result["North"]["Electronics"] == 2
    assert result["East"]["Food"] == 2
    assert result["West"]["Clothing"] == 2


def test_pivot_quarter_by_category_sum():
    records = load_records()
    result = pivot(records, "quarter", "category", "amount", "sum")
    assert abs(result["Q1"]["Electronics"] - 2180.0) < 0.01
    assert abs(result["Q3"]["Clothing"] - 1470.0) < 0.01
    assert abs(result["Q4"]["Food"] - 1040.0) < 0.01


def test_pivot_missing_combination_is_zero():
    records = [
        {"region": "North", "category": "Electronics", "amount": 100.0, "quarter": "Q1"},
        {"region": "South", "category": "Clothing", "amount": 200.0, "quarter": "Q2"},
    ]
    result = pivot(records, "region", "category", "amount", "sum")
    assert result["North"]["Clothing"] == 0
    assert result["South"]["Electronics"] == 0


def test_pivot_to_table_headers():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "sum")
    table = pivot_to_table(result)
    assert table[0] == ["", "Clothing", "Electronics", "Food"]


def test_pivot_to_table_rows_sorted():
    records = load_records()
    result = pivot(records, "region", "category", "amount", "sum")
    table = pivot_to_table(result)
    row_names = [row[0] for row in table[1:]]
    assert row_names == ["East", "North", "South", "West"]
    assert abs(table[1][2] - 2900.0) < 0.01
