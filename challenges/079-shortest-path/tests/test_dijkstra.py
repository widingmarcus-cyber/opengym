"""Tests for Challenge 079: Shortest Path."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

from dijkstra import shortest_path, all_distances


def test_shortest_path_simple():
    graph = {
        "a": [("b", 1), ("c", 4)],
        "b": [("c", 2), ("d", 5)],
        "c": [("d", 1)],
        "d": [],
    }
    path, dist = shortest_path(graph, "a", "d")
    assert path == ["a", "b", "c", "d"]
    assert dist == 4


def test_shortest_path_direct():
    graph = {"a": [("b", 3)], "b": []}
    path, dist = shortest_path(graph, "a", "b")
    assert path == ["a", "b"]
    assert dist == 3


def test_shortest_path_unreachable():
    graph = {"a": [("b", 1)], "b": [], "c": []}
    path, dist = shortest_path(graph, "a", "c")
    assert path == []
    assert dist == float("inf")


def test_shortest_path_same_node():
    graph = {"a": [("b", 1)], "b": []}
    path, dist = shortest_path(graph, "a", "a")
    assert path == ["a"]
    assert dist == 0


def test_shortest_path_multiple_routes():
    graph = {
        "a": [("b", 1), ("c", 10)],
        "b": [("c", 1)],
        "c": [],
    }
    path, dist = shortest_path(graph, "a", "c")
    assert path == ["a", "b", "c"]
    assert dist == 2


def test_shortest_path_self_loop():
    graph = {"a": [("a", 0), ("b", 5)], "b": []}
    path, dist = shortest_path(graph, "a", "b")
    assert path == ["a", "b"]
    assert dist == 5


def test_all_distances_simple():
    graph = {
        "a": [("b", 1), ("c", 4)],
        "b": [("c", 2), ("d", 5)],
        "c": [("d", 1)],
        "d": [],
    }
    result = all_distances(graph, "a")
    assert result == {"a": 0, "b": 1, "c": 3, "d": 4}


def test_all_distances_unreachable():
    graph = {"a": [("b", 1)], "b": [], "c": [("d", 1)], "d": []}
    result = all_distances(graph, "a")
    assert result == {"a": 0, "b": 1}


def test_all_distances_single_node():
    graph = {"a": []}
    result = all_distances(graph, "a")
    assert result == {"a": 0}


def test_shortest_path_zero_weight():
    graph = {"a": [("b", 0), ("c", 1)], "b": [("c", 0)], "c": []}
    path, dist = shortest_path(graph, "a", "c")
    assert path == ["a", "b", "c"]
    assert dist == 0
