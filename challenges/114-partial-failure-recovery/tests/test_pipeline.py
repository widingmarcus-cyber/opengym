import sys
import json
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from pipeline import process_record, process_all

def test_all_records_process():
    """All 10 records should process without exceptions."""
    results = process_all("data.json", "output.json")
    assert len(results) == 10

def test_standard_usd():
    """Record 1: standard USD 100.00 -> 100.0"""
    record = {"id": 1, "type": "standard", "value": "100.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 100.0

def test_premium_type():
    """Record 6: premium USD 1000.00 -> 1500.0 (1.5x multiplier)"""
    record = {"id": 6, "type": "premium", "value": "1000.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 1500.0

def test_express_type():
    """Record 8: express USD 300.00 -> 375.0 (1.25x multiplier)"""
    record = {"id": 8, "type": "express", "value": "300.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 375.0

def test_negative_value():
    """Record 4: negative value should be treated as absolute value."""
    record = {"id": 4, "type": "standard", "value": "-50.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 50.0

def test_eur_conversion():
    """Record 2: standard EUR 250.50 -> 275.55"""
    record = {"id": 2, "type": "standard", "value": "250.50", "currency": "EUR"}
    result = process_record(record)
    assert result["usd_value"] == 275.55

def test_value_with_text():
    """Record 10: value '425.00 USD' should parse as 425.00"""
    record = {"id": 10, "type": "standard", "value": "425.00 USD", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 425.0

def test_zero_value():
    """Record 7: zero value should work fine."""
    record = {"id": 7, "type": "standard", "value": "0", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 0.0

def test_process_all_returns_exactly_10():
    """process_all must return a list of exactly 10 results from data.json."""
    results = process_all("data.json", "output.json")
    assert isinstance(results, list), "process_all should return a list"
    assert len(results) == 10, f"Expected 10 results, got {len(results)}"
    ids = [r["id"] for r in results]
    assert sorted(ids) == list(range(1, 11)), f"Expected IDs 1-10, got {sorted(ids)}"

def test_express_multiplier_exact():
    """Express type must apply exactly a 1.25x multiplier (not 1.0 or any other)."""
    record = {"id": 8, "type": "express", "value": "400.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 500.0, (
        f"express 400.00 USD should be 500.0 (400*1.25), got {result['usd_value']}"
    )

def test_negative_value_returns_positive():
    """Negative values must be converted to absolute value, not raise errors."""
    record = {"id": 99, "type": "standard", "value": "-200.00", "currency": "USD"}
    result = process_record(record)
    assert result["usd_value"] == 200.0, (
        f"Negative -200.00 should become 200.0, got {result['usd_value']}"
    )

def test_value_with_currency_suffix():
    """Value strings with trailing text like '125.50 EUR' must parse the number."""
    record = {"id": 99, "type": "standard", "value": "125.50 EUR", "currency": "EUR"}
    result = process_record(record)
    expected = round(125.50 * 1.1, 2)
    assert result["usd_value"] == expected, (
        f"'125.50 EUR' should parse as 125.50 then convert, expected {expected}, got {result['usd_value']}"
    )
