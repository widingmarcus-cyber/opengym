"""Tests for Challenge 097: End to End Pipeline."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from pipeline import ingest, validate, transform, report

RAW_DIR = str(Path(__file__).parent.parent / "setup" / "raw_data")


def test_ingest_returns_dict():
    data = ingest(RAW_DIR)
    assert isinstance(data, dict)
    assert "users" in data
    assert "transactions" in data
    assert "products" in data


def test_ingest_reads_rows():
    data = ingest(RAW_DIR)
    assert len(data["users"]) == 8
    assert len(data["transactions"]) == 12
    assert len(data["products"]) == 6


def test_validate_removes_invalid_users():
    data = ingest(RAW_DIR)
    clean, errors = validate(data)
    for user in clean["users"]:
        assert user["id"] != ""
        assert user["name"] != ""
        assert "@" in user["email"]


def test_validate_removes_invalid_transactions():
    data = ingest(RAW_DIR)
    clean, errors = validate(data)
    for txn in clean["transactions"]:
        assert txn["user_id"] != ""
        assert float(txn["amount"]) > 0


def test_validate_removes_duplicate_products():
    data = ingest(RAW_DIR)
    clean, errors = validate(data)
    product_ids = [p["id"] for p in clean["products"]]
    assert len(product_ids) == len(set(product_ids))


def test_validate_reports_errors():
    data = ingest(RAW_DIR)
    clean, errors = validate(data)
    assert len(errors) > 0
    for err in errors:
        assert "source" in err
        assert "row" in err
        assert "reason" in err


def test_transform_user_spending():
    data = ingest(RAW_DIR)
    clean, _ = validate(data)
    transformed = transform(clean)
    assert "user_spending" in transformed
    spending = transformed["user_spending"]
    assert isinstance(spending, list)
    assert all("user_id" in s and "total" in s for s in spending)


def test_report_summary():
    data = ingest(RAW_DIR)
    clean, _ = validate(data)
    transformed = transform(clean)
    summary = report(transformed)
    assert "total_revenue" in summary
    assert "active_users" in summary
    assert "top_products" in summary
    assert isinstance(summary["total_revenue"], (int, float))
    assert isinstance(summary["active_users"], int)
    assert summary["active_users"] > 0
    assert summary["total_revenue"] > 0
    assert len(summary["top_products"]) <= 3
