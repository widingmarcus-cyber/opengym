"""Tests for Challenge 029: Debug the Flaky Test."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from processor import process_items, get_processed_count, get_processed_items
from cache import clear_cache, get_cache


def test_process_basic():
    """Processing [1, 2, 3] should return [2, 4, 6]."""
    results = process_items([1, 2, 3])
    assert results == [2, 4, 6]


def test_process_count_after_basic():
    """After processing 3 items, cache count should be 3."""
    process_items([1, 2, 3])
    assert get_processed_count() == 3


def test_process_single():
    """Processing a single item should work and cache should have 1 item."""
    results = process_items([5])
    assert results == [10]
    assert get_processed_count() == 1


def test_process_empty():
    """Processing empty list should return empty and cache should be empty."""
    results = process_items([])
    assert results == []
    assert get_processed_count() == 0


def test_cached_items_match_results():
    """Cached items should match the most recent process_items call."""
    process_items([10, 20])
    cached = get_processed_items()
    assert cached == [20, 40]


def test_cache_resets_between_calls():
    """Each call to process_items should start with a fresh cache."""
    process_items([1, 2, 3])
    process_items([4, 5])
    assert get_processed_count() == 2
    assert get_processed_items() == [8, 10]


def test_clear_cache_works():
    """clear_cache() should actually empty the cache."""
    process_items([1, 2, 3])
    clear_cache()
    assert get_cache() == []
    assert len(get_cache()) == 0


def test_sequential_independence():
    """Multiple sequential process calls should be independent."""
    r1 = process_items([100])
    assert r1 == [200]
    assert get_processed_count() == 1

    r2 = process_items([1, 2, 3, 4, 5])
    assert r2 == [2, 4, 6, 8, 10]
    assert get_processed_count() == 5

    r3 = process_items([])
    assert r3 == []
    assert get_processed_count() == 0
