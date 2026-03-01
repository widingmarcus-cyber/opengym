"""Test suite for processor module.

These tests pass individually but fail when run together due to
shared mutable state. This file is for reference - the actual
verification tests are in tests/.
"""

from processor import process_items, get_processed_count, get_processed_items


def test_process_basic():
    results = process_items([1, 2, 3])
    assert results == [2, 4, 6]
    assert get_processed_count() == 3


def test_process_single():
    results = process_items([5])
    assert results == [10]
    assert get_processed_count() == 1


def test_process_empty():
    results = process_items([])
    assert results == []
    assert get_processed_count() == 0


def test_cached_items_match():
    process_items([10, 20])
    cached = get_processed_items()
    assert cached == [20, 40]
