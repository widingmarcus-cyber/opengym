# Challenge 155: Subtask Partial Failure Propagation

**Difficulty:** Hard
**Category:** task-splitting
**Dimension:** multi-agent
**Type:** Multi-session (2 steps)

## Objective

Execute a batch of subtasks where some may fail. Correctly identify successes and failures, and propagate partial failure information to a summary.

## What This Tests

- Processing a batch of subtasks with mixed success/failure outcomes
- Handling invalid inputs gracefully (marking as failed, not crashing)
- Correctly computing outputs for valid inputs
- Summarizing partial failures with accurate counts

## Sessions

1. **Executor** -- Read `setup/subtasks.json` (5 subtasks). Each "compute" task squares the input. Input of -1 is invalid (negative not allowed). Write results to `setup/results.json` with status and output for each subtask.
2. **Summarizer** -- Read `setup/results.json`. Write `setup/answer.json` with `{"total_succeeded": 4, "total_failed": 1, "failed_ids": [3]}`.

## Constraints

- `setup/subtasks.json` is pre-created with 5 subtasks.
- `setup/results.json` must have 5 entries with correct statuses.
- Subtask 3 (input=-1) must have `status="failed"`.
- Subtasks 1, 2, 4, 5 must have correct squared outputs (100, 400, 1600, 2500).
- `setup/answer.json` must have `total_succeeded=4`, `total_failed=1`, `failed_ids=[3]`.
