"""Tests for Challenge 051: REST Pagination Client."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from fake_api import PaginatedAPI
from client import fetch_all_items, fetch_page_range


def test_fetch_all_single_page():
    api = PaginatedAPI([1, 2, 3], page_size=5)
    result = fetch_all_items(api)
    assert result == [1, 2, 3]


def test_fetch_all_multiple_pages():
    api = PaginatedAPI([1, 2, 3, 4, 5, 6, 7], page_size=3)
    result = fetch_all_items(api)
    assert result == [1, 2, 3, 4, 5, 6, 7]


def test_fetch_all_empty():
    api = PaginatedAPI([], page_size=3)
    result = fetch_all_items(api)
    assert result == []


def test_fetch_all_exact_pages():
    api = PaginatedAPI([10, 20, 30, 40, 50, 60], page_size=3)
    result = fetch_all_items(api)
    assert result == [10, 20, 30, 40, 50, 60]


def test_fetch_page_range_middle():
    api = PaginatedAPI(list(range(1, 16)), page_size=3)
    result = fetch_page_range(api, 2, 4)
    assert result == [4, 5, 6, 7, 8, 9, 10, 11, 12]


def test_fetch_page_range_single_page():
    api = PaginatedAPI(list(range(1, 10)), page_size=3)
    result = fetch_page_range(api, 2, 2)
    assert result == [4, 5, 6]


def test_fetch_page_range_clamps_to_valid():
    api = PaginatedAPI([1, 2, 3, 4, 5], page_size=2)
    result = fetch_page_range(api, 2, 10)
    assert result == [3, 4, 5]


def test_fetch_page_range_out_of_range_returns_empty():
    api = PaginatedAPI([1, 2, 3], page_size=3)
    result = fetch_page_range(api, 5, 10)
    assert result == []
