"""Tests for Challenge 033: Aggregate JSON Logs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from analyzer import count_by_level, error_rate, busiest_hour, messages_containing

DATA_FILE = str(Path(__file__).parent.parent / "setup" / "logs.jsonl")


def test_count_by_level_returns_dict():
    result = count_by_level(DATA_FILE)
    assert isinstance(result, dict)
    assert set(result.keys()) == {"INFO", "WARN", "ERROR"}


def test_count_by_level_values():
    result = count_by_level(DATA_FILE)
    assert result["INFO"] == 38
    assert result["WARN"] == 8
    assert result["ERROR"] == 6


def test_count_by_level_total():
    result = count_by_level(DATA_FILE)
    assert sum(result.values()) == 52


def test_error_rate_value():
    rate = error_rate(DATA_FILE)
    assert isinstance(rate, float)
    assert abs(rate - 6 / 52) < 1e-6


def test_error_rate_range():
    rate = error_rate(DATA_FILE)
    assert 0.0 <= rate <= 1.0


def test_busiest_hour():
    hour = busiest_hour(DATA_FILE)
    assert hour == 10


def test_messages_containing_database():
    results = messages_containing(DATA_FILE, "database")
    assert len(results) == 6
    assert all("database" in msg.lower() for msg in results)


def test_messages_containing_failed():
    results = messages_containing(DATA_FILE, "failed")
    assert len(results) == 4
    assert all("failed" in msg.lower() for msg in results)
