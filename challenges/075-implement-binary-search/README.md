# Challenge 075: Implement Binary Search

## Difficulty: Easy

## Task

The file `setup/binary_search.py` contains stubs. Implement three binary search functions that operate on sorted lists.

## Requirements

1. `binary_search(arr, target) -> int` -- Return the index of `target` in the sorted list `arr`, or `-1` if not found. If there are duplicates, return any valid index.
2. `bisect_left(arr, target) -> int` -- Return the leftmost insertion point for `target` in `arr`. This is the index of the first element that is not less than `target`.
3. `bisect_right(arr, target) -> int` -- Return the rightmost insertion point for `target` in `arr`. This is the index past the last element that is not greater than `target`.

All functions must correctly handle duplicates, empty lists, and single-element lists.

## Rules

- Only modify files in the `setup/` directory
- Do not use Python's built-in `bisect` module

## Examples

```python
binary_search([1, 3, 5, 7, 9], 5)      # 2
binary_search([1, 3, 5, 7, 9], 4)      # -1
bisect_left([1, 3, 3, 3, 5], 3)        # 1
bisect_right([1, 3, 3, 3, 5], 3)       # 4
bisect_left([], 5)                       # 0
```
