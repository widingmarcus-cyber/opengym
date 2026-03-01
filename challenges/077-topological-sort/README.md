# Challenge 077: Topological Sort

## Difficulty: Medium

## Task

The file `setup/topo_sort.py` contains stubs. Implement three functions for working with directed acyclic graphs (DAGs).

## Requirements

1. `topological_sort(graph: dict[str, list[str]]) -> list[str]` -- Perform a topological sort on a directed graph. The graph is an adjacency list where each key maps to a list of nodes it depends on (i.e., edges point from dependency to dependent). Return a valid topological ordering where each node appears after all its dependencies. Raise `ValueError` if the graph contains a cycle.
2. `has_cycle(graph: dict[str, list[str]]) -> bool` -- Return `True` if the directed graph contains a cycle, `False` otherwise.
3. `all_paths(graph: dict[str, list[str]], start: str, end: str) -> list[list[str]]` -- Return all possible paths from `start` to `end` in the graph. Each path is a list of nodes from start to end. Return an empty list if no path exists. The graph for this function is treated as a forward adjacency list (key -> list of nodes it points to).

## Rules

- Only modify files in the `setup/` directory
- The topological sort must produce a valid ordering (not necessarily unique)

## Examples

```python
graph = {"a": [], "b": ["a"], "c": ["a", "b"]}
topological_sort(graph)  # ["a", "b", "c"] (one valid ordering)

has_cycle({"a": ["b"], "b": ["a"]})  # True

forward = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
all_paths(forward, "a", "d")  # [["a", "b", "d"], ["a", "c", "d"]]
```
