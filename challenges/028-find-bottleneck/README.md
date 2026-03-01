# Challenge 028: Find the Bottleneck

## Difficulty: Easy

## Task

A search function is unacceptably slow. You have been given profiling output (`setup/profiler_output.txt`) and the source code (`setup/search.py`).

Your job is to read the profiling data, identify the performance bottleneck, and optimize the code so it runs efficiently.

## Files

```
setup/
  profiler_output.txt   # Simulated cProfile output showing the hotspot
  search.py             # The search module to optimize
```

## What to Do

1. Read the profiler output to identify which function is the bottleneck
2. Read the source code and understand why it is slow
3. Rewrite the slow code to be fast while keeping the same interface and behavior

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- The `build_index(products)` function must still accept a list of product dicts
- The `search(index, query)` function must still return a list of matching product dicts
- All existing behavior must be preserved (case-insensitive search, partial matching)
