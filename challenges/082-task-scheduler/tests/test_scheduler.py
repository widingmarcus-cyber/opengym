"""Tests for Challenge 082: Task Scheduler."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from scheduler import TaskScheduler


def test_single_task():
    s = TaskScheduler()
    s.add_task("a", priority=1, duration=5)
    assert s.schedule() == ["a"]
    assert s.total_duration() == 5


def test_no_dependencies_priority_order():
    s = TaskScheduler()
    s.add_task("low", priority=1)
    s.add_task("high", priority=3)
    s.add_task("mid", priority=2)
    result = s.schedule()
    assert result == ["high", "mid", "low"]


def test_linear_chain():
    s = TaskScheduler()
    s.add_task("a", priority=1, duration=2)
    s.add_task("b", priority=2, dependencies=["a"], duration=3)
    s.add_task("c", priority=3, dependencies=["b"], duration=1)
    result = s.schedule()
    assert result == ["a", "b", "c"]
    assert s.total_duration() == 6


def test_diamond_dependencies():
    s = TaskScheduler()
    s.add_task("a", priority=1, duration=1)
    s.add_task("b", priority=2, dependencies=["a"], duration=2)
    s.add_task("c", priority=3, dependencies=["a"], duration=3)
    s.add_task("d", priority=4, dependencies=["b", "c"], duration=1)
    result = s.schedule()
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")


def test_priority_among_available():
    s = TaskScheduler()
    s.add_task("base", priority=1, duration=1)
    s.add_task("high", priority=10, dependencies=["base"], duration=1)
    s.add_task("low", priority=2, dependencies=["base"], duration=1)
    result = s.schedule()
    assert result[0] == "base"
    assert result.index("high") < result.index("low")


def test_circular_dependency_raises():
    s = TaskScheduler()
    s.add_task("a", priority=1, dependencies=["b"])
    s.add_task("b", priority=1, dependencies=["a"])
    with pytest.raises(ValueError):
        s.schedule()


def test_total_duration():
    s = TaskScheduler()
    s.add_task("a", priority=1, duration=3)
    s.add_task("b", priority=2, duration=5)
    s.add_task("c", priority=3, duration=2)
    s.schedule()
    assert s.total_duration() == 10


def test_critical_path_linear():
    s = TaskScheduler()
    s.add_task("a", priority=1, duration=2)
    s.add_task("b", priority=2, dependencies=["a"], duration=3)
    s.add_task("c", priority=3, dependencies=["b"], duration=4)
    s.schedule()
    assert s.get_critical_path() == ["a", "b", "c"]


def test_critical_path_branches():
    s = TaskScheduler()
    s.add_task("root", priority=1, duration=1)
    s.add_task("short", priority=2, dependencies=["root"], duration=1)
    s.add_task("long1", priority=3, dependencies=["root"], duration=5)
    s.add_task("long2", priority=4, dependencies=["long1"], duration=3)
    s.schedule()
    path = s.get_critical_path()
    assert path[0] == "root"
    assert "long1" in path
    assert "long2" in path


def test_three_way_cycle_raises():
    s = TaskScheduler()
    s.add_task("a", priority=1, dependencies=["c"])
    s.add_task("b", priority=2, dependencies=["a"])
    s.add_task("c", priority=3, dependencies=["b"])
    with pytest.raises(ValueError):
        s.schedule()
