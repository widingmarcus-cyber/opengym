"""Tests for Challenge 042: Convert Callbacks to Async."""

import sys
import asyncio
import inspect
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from pipeline import fetch_data, process_data, save_results, run_pipeline


# --- Test that all functions are proper coroutines ---

def test_fetch_data_is_coroutine():
    assert inspect.iscoroutinefunction(fetch_data), "fetch_data must be an async function"


def test_process_data_is_coroutine():
    assert inspect.iscoroutinefunction(process_data), "process_data must be an async function"


def test_save_results_is_coroutine():
    assert inspect.iscoroutinefunction(save_results), "save_results must be an async function"


# --- Test individual async functions ---

def test_fetch_data_returns_correct_structure():
    result = asyncio.run(fetch_data("https://example.com/api"))
    assert result["url"] == "https://example.com/api"
    assert result["status"] == "ok"
    assert isinstance(result["data"], list)
    assert len(result["data"]) == 20


def test_fetch_data_deterministic():
    r1 = asyncio.run(fetch_data("https://example.com/api"))
    r2 = asyncio.run(fetch_data("https://example.com/api"))
    assert r1["data"] == r2["data"]


def test_process_data_filters_and_transforms():
    seed = int(hashlib.md5(b"https://example.com/api").hexdigest()[:8], 16)
    data = [(seed * (i + 1) * 7 + 13) % 1000 for i in range(20)]
    result = asyncio.run(process_data(data))

    expected_filtered = [x for x in data if x > 100]
    expected_transformed = [round(x * 1.15 + 10, 2) for x in expected_filtered]

    assert result["filtered"] == expected_filtered
    assert result["transformed"] == expected_transformed
    assert result["total"] == round(sum(expected_transformed), 2)
    assert result["count"] == len(expected_transformed)


def test_save_results_returns_confirmation():
    results = {"total": 1234.56, "count": 10}
    confirmation = asyncio.run(save_results(results))
    assert confirmation["saved"] is True
    assert confirmation["record_count"] == 10
    assert "timestamp" in confirmation


# --- Test the full pipeline ---

def test_run_pipeline_end_to_end():
    confirmation = asyncio.run(run_pipeline("https://example.com/data"))
    assert confirmation["saved"] is True
    assert isinstance(confirmation["record_count"], int)
    assert confirmation["record_count"] > 0
    assert "timestamp" in confirmation
