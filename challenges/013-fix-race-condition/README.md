# Challenge 013: Fix the Race Condition

## Difficulty: Medium

## Task

The file `setup/task_queue.py` implements a `TaskQueue` class that processes tasks concurrently using threads. However, results are silently dropped because the shared results dictionary has no synchronization.

When multiple threads write to the results dict simultaneously, some results go missing. The task queue appears to work for small inputs but fails with larger workloads.

**Your job:** Add proper synchronization so that all task results are correctly collected.

## Class: TaskQueue

- `__init__(self, num_workers)` -- Creates a task queue with the specified number of worker threads
- `submit(self, task_id, func, *args)` -- Submits a task to be processed
- `process_all(self)` -- Processes all submitted tasks using worker threads
- `get_results(self)` -- Returns a dict mapping task_id to result

## Rules

- Only modify files in the `setup/` directory
- Do not change the public API (class name, method signatures)
- All submitted tasks must have their results collected
- The solution must still use threads (do not convert to single-threaded)
