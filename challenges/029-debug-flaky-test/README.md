# Challenge 029: Debug the Flaky Test

## Difficulty: Medium

## Task

A test suite has a flaky test problem: each test passes when run individually, but they fail when run together. The issue is shared mutable state between tests.

Your job is to find and fix the shared state problem so all tests pass reliably regardless of execution order.

## Files

```
setup/
  cache.py                  # A caching module with module-level state
  processor.py              # Data processor that uses the cache
  test_processor_broken.py  # The broken test file (for reference)
```

## What to Do

1. Read the test file to understand what is being tested
2. Identify the shared mutable state that causes tests to interfere with each other
3. Fix the code so that each processing call starts with a clean state

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- The `process_items()` function must still use caching
- The `get_cache()` function must still return the current cache contents
- The `clear_cache()` function must exist and work correctly
- Tests must pass regardless of execution order
