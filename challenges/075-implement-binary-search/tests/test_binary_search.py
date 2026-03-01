"""Tests for Challenge 075: Implement Binary Search."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from binary_search import binary_search, bisect_left, bisect_right


def test_binary_search_found():
    assert binary_search([1, 3, 5, 7, 9], 5) == 2


def test_binary_search_not_found():
    assert binary_search([1, 3, 5, 7, 9], 4) == -1


def test_binary_search_empty_list():
    assert binary_search([], 5) == -1


def test_binary_search_single_element_found():
    assert binary_search([42], 42) == 0


def test_binary_search_single_element_not_found():
    assert binary_search([42], 7) == -1


def test_binary_search_all_same():
    result = binary_search([3, 3, 3, 3, 3], 3)
    assert 0 <= result <= 4


def test_binary_search_first_and_last():
    assert binary_search([10, 20, 30, 40, 50], 10) == 0
    assert binary_search([10, 20, 30, 40, 50], 50) == 4


def test_bisect_left_with_duplicates():
    assert bisect_left([1, 3, 3, 3, 5], 3) == 1


def test_bisect_right_with_duplicates():
    assert bisect_right([1, 3, 3, 3, 5], 3) == 4


def test_bisect_left_and_right_edge_cases():
    assert bisect_left([], 5) == 0
    assert bisect_right([], 5) == 0
    assert bisect_left([1, 2, 3], 0) == 0
    assert bisect_right([1, 2, 3], 0) == 0
    assert bisect_left([1, 2, 3], 4) == 3
    assert bisect_right([1, 2, 3], 4) == 3
    assert bisect_left([5, 5, 5], 5) == 0
    assert bisect_right([5, 5, 5], 5) == 3
