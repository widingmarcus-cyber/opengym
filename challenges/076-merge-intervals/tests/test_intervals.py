"""Tests for Challenge 076: Merge Intervals."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from intervals import merge, has_overlap, total_covered


def test_merge_overlapping():
    assert merge([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]


def test_merge_adjacent():
    assert merge([(1, 4), (4, 5)]) == [(1, 5)]


def test_merge_empty():
    assert merge([]) == []


def test_merge_single():
    assert merge([(3, 7)]) == [(3, 7)]


def test_merge_all_overlapping():
    assert merge([(1, 5), (2, 6), (3, 7), (4, 8)]) == [(1, 8)]


def test_merge_none_overlapping():
    assert merge([(1, 2), (5, 6), (9, 10)]) == [(1, 2), (5, 6), (9, 10)]


def test_has_overlap_true():
    assert has_overlap([(1, 4), (3, 6)]) is True


def test_has_overlap_false():
    assert has_overlap([(1, 3), (5, 7)]) is False


def test_has_overlap_adjacent():
    assert has_overlap([(1, 3), (3, 5)]) is True


def test_has_overlap_empty():
    assert has_overlap([]) is False


def test_total_covered_with_overlaps():
    assert total_covered([(1, 3), (2, 5), (8, 10)]) == 6


def test_total_covered_no_overlaps():
    assert total_covered([(1, 3), (5, 7)]) == 4


def test_total_covered_empty():
    assert total_covered([]) == 0


def test_merge_unsorted_input():
    assert merge([(8, 10), (1, 3), (2, 6)]) == [(1, 6), (8, 10)]
