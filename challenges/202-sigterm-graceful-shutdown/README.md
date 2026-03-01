# Challenge 202: SIGTERM Graceful Shutdown

## Difficulty: Hard
## Category: Failure Recovery

## Description

A long-running worker (`setup/worker.py`) processes tasks from `setup/task_queue.json`. When it receives SIGTERM, it should save its progress and exit cleanly. Currently the worker has NO signal handling — it just dies and loses all progress.

Your job:
1. Add SIGTERM (and SIGINT) signal handling to `setup/worker.py` so that:
   - When a shutdown signal is received, it finishes the current task (does not abort mid-task)
   - It saves completed results to `setup/completed.json`
   - It saves the remaining unprocessed tasks to `setup/remaining.json`
   - It writes a shutdown report to `setup/shutdown_report.json`
2. The worker must process tasks by reading each task object, computing `result = task["a"] * task["b"] + task["c"]`, and storing the result.
3. Simulate a graceful shutdown: process exactly the first 5 tasks (out of 10), then save state as if SIGTERM was received after task 5.

## Expected Output

- `setup/worker.py` — updated with signal handling code
- `setup/completed.json` — array of the first 5 task results, each with `task_id`, `a`, `b`, `c`, `result`
- `setup/remaining.json` — array of the remaining 5 unprocessed tasks
- `setup/shutdown_report.json` — JSON with keys: `tasks_completed` (5), `tasks_remaining` (5), `shutdown_reason` ("SIGTERM"), `clean_shutdown` (true)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
