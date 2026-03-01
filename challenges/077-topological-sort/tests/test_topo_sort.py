"""Tests for Challenge 077: Topological Sort."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

import pytest
from topo_sort import topological_sort, has_cycle, all_paths


def test_topological_sort_simple_chain():
    graph = {"a": [], "b": ["a"], "c": ["b"]}
    result = topological_sort(graph)
    assert result.index("a") < result.index("b") < result.index("c")


def test_topological_sort_diamond():
    graph = {"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}
    result = topological_sort(graph)
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")


def test_topological_sort_single_node():
    graph = {"a": []}
    assert topological_sort(graph) == ["a"]


def test_topological_sort_disconnected():
    graph = {"a": [], "b": [], "c": []}
    result = topological_sort(graph)
    assert set(result) == {"a", "b", "c"}
    assert len(result) == 3


def test_topological_sort_cycle_raises():
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
    with pytest.raises(ValueError):
        topological_sort(graph)


def test_has_cycle_true():
    graph = {"a": ["b"], "b": ["a"]}
    assert has_cycle(graph) is True


def test_has_cycle_false():
    graph = {"a": [], "b": ["a"], "c": ["b"]}
    assert has_cycle(graph) is False


def test_has_cycle_self_loop():
    graph = {"a": ["a"]}
    assert has_cycle(graph) is True


def test_all_paths_diamond():
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    result = all_paths(graph, "a", "d")
    paths = [tuple(p) for p in result]
    assert set(paths) == {("a", "b", "d"), ("a", "c", "d")}


def test_all_paths_no_path():
    graph = {"a": ["b"], "b": [], "c": []}
    result = all_paths(graph, "a", "c")
    assert result == []
