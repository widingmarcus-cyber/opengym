# Challenge 076: Merge Intervals

## Difficulty: Easy

## Task

The file `setup/intervals.py` contains stubs. Implement three functions for working with intervals represented as `(start, end)` tuples.

## Requirements

1. `merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]` -- Takes a list of `(start, end)` tuples and returns a new list of merged non-overlapping intervals, sorted by start value. Overlapping or adjacent intervals should be combined.
2. `has_overlap(intervals: list[tuple[int, int]]) -> bool` -- Return `True` if any two intervals in the list overlap, `False` otherwise. Adjacent intervals (e.g., `(1, 3)` and `(3, 5)`) count as overlapping.
3. `total_covered(intervals: list[tuple[int, int]]) -> int` -- Return the total length covered by all intervals combined (after merging overlaps).

## Rules

- Only modify files in the `setup/` directory
- Intervals are inclusive of start and exclusive of end for length calculation purposes: `total_covered([(1, 4)]) == 3`

## Examples

```python
merge([(1, 3), (2, 6), (8, 10)])        # [(1, 6), (8, 10)]
merge([(1, 4), (4, 5)])                  # [(1, 5)]
has_overlap([(1, 3), (5, 7)])            # False
has_overlap([(1, 4), (3, 6)])            # True
total_covered([(1, 3), (2, 5), (8, 10)]) # 6
```
