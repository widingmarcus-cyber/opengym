# Challenge 038: Compute Running Stats

## Difficulty: Easy

## Task

Implement a streaming statistics calculator in `setup/stats.py`. The class must compute statistics incrementally without storing all values in memory.

## Requirements

Implement a `RunningStats` class in `setup/stats.py` with the following methods:

1. `update(value)` -- Add a new numeric value to the running computation
2. `mean()` -- Return the current mean as a float
3. `variance()` -- Return the current population variance as a float
4. `std_dev()` -- Return the current population standard deviation as a float
5. `count()` -- Return the number of values seen so far as an int
6. `min()` -- Return the minimum value seen so far as a float
7. `max()` -- Return the maximum value seen so far as a float

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- The implementation must be memory-efficient: do not store all values in a list or array. Use Welford's online algorithm or a similar approach for computing variance incrementally.
- `mean()`, `variance()`, and `std_dev()` should raise `ValueError` if no values have been added yet
- `min()` and `max()` should raise `ValueError` if no values have been added yet

## Examples

```python
rs = RunningStats()
rs.update(10)
rs.update(20)
rs.update(30)
rs.mean()       # 20.0
rs.variance()   # 66.666...
rs.std_dev()    # 8.164...
rs.count()      # 3
rs.min()        # 10.0
rs.max()        # 30.0
```
