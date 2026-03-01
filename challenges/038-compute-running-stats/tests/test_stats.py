"""Tests for Challenge 038: Compute Running Stats."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from stats import RunningStats


def test_single_value():
    rs = RunningStats()
    rs.update(42)
    assert rs.count() == 1
    assert abs(rs.mean() - 42.0) < 1e-9
    assert abs(rs.variance() - 0.0) < 1e-9
    assert abs(rs.std_dev() - 0.0) < 1e-9
    assert abs(rs.min() - 42.0) < 1e-9
    assert abs(rs.max() - 42.0) < 1e-9


def test_basic_stats():
    rs = RunningStats()
    for v in [10, 20, 30]:
        rs.update(v)
    assert rs.count() == 3
    assert abs(rs.mean() - 20.0) < 1e-9
    assert abs(rs.variance() - 200.0 / 3) < 1e-6
    assert abs(rs.std_dev() - math.sqrt(200.0 / 3)) < 1e-6


def test_min_and_max():
    rs = RunningStats()
    for v in [5, 1, 9, 3, 7]:
        rs.update(v)
    assert abs(rs.min() - 1.0) < 1e-9
    assert abs(rs.max() - 9.0) < 1e-9


def test_negative_numbers():
    rs = RunningStats()
    for v in [-5, -10, -15]:
        rs.update(v)
    assert abs(rs.mean() - (-10.0)) < 1e-9
    assert abs(rs.variance() - 50.0 / 3) < 1e-6
    assert abs(rs.min() - (-15.0)) < 1e-9
    assert abs(rs.max() - (-5.0)) < 1e-9


def test_large_dataset():
    rs = RunningStats()
    values = list(range(1, 1001))
    for v in values:
        rs.update(v)
    assert rs.count() == 1000
    assert abs(rs.mean() - 500.5) < 1e-6
    assert abs(rs.min() - 1.0) < 1e-9
    assert abs(rs.max() - 1000.0) < 1e-9


def test_empty_raises_on_mean():
    rs = RunningStats()
    try:
        rs.mean()
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_empty_raises_on_variance():
    rs = RunningStats()
    try:
        rs.variance()
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_empty_raises_on_min_max():
    rs = RunningStats()
    try:
        rs.min()
        assert False, "Expected ValueError"
    except ValueError:
        pass
    try:
        rs.max()
        assert False, "Expected ValueError"
    except ValueError:
        pass
