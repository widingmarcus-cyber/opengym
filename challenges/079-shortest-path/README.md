# Challenge 079: Shortest Path

## Difficulty: Medium

## Task

The file `setup/dijkstra.py` contains stubs. Implement Dijkstra's shortest path algorithm and a related utility function.

## Requirements

1. `shortest_path(graph: dict, start: str, end: str) -> tuple[list[str], float]` -- Find the shortest path in a weighted directed graph. The graph is represented as `{node: [(neighbor, weight), ...]}`. Return a tuple of `(path, distance)` where `path` is the list of nodes from `start` to `end` and `distance` is the total weight. If no path exists, return `([], float('inf'))`.
2. `all_distances(graph: dict, start: str) -> dict[str, float]` -- Return a dictionary mapping every reachable node to its shortest distance from `start`. Unreachable nodes should not appear in the result. The start node should have distance `0`.

## Rules

- Only modify files in the `setup/` directory
- All edge weights are non-negative
- The algorithm should handle graphs where not all nodes are reachable

## Examples

```python
graph = {
    "a": [("b", 1), ("c", 4)],
    "b": [("c", 2), ("d", 5)],
    "c": [("d", 1)],
    "d": []
}
shortest_path(graph, "a", "d")   # (["a", "b", "c", "d"], 4)
all_distances(graph, "a")        # {"a": 0, "b": 1, "c": 3, "d": 4}
```
