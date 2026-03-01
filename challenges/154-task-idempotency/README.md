# Challenge 154: Task Idempotency

**Difficulty:** Medium
**Category:** task-splitting
**Dimension:** multi-agent
**Type:** Multi-session (3 steps)

## Objective

Demonstrate idempotent task processing: if the same task is delivered twice, it should only be processed once. New tasks should still be processed normally.

## What This Tests

- Tracking processed tasks to ensure idempotency
- Skipping duplicate task deliveries
- Correctly processing new tasks while rejecting duplicates
- Maintaining an accurate counter across multiple task deliveries

## Sessions

1. **Process Task 1** -- Process task `{"id": "task_001", "action": "increment_counter"}`. Write to `setup/results.json`: `{"counter": 1}`. Record `task_001` in `setup/processed.json`.
2. **Duplicate Delivery** -- Same task delivered again: `{"id": "task_001", "action": "increment_counter"}`. Check `setup/processed.json` and skip it (already processed). Counter must stay at 1.
3. **Process Task 2** -- New task `{"id": "task_002", "action": "increment_counter"}`. Counter becomes 2. Write the final counter value to `setup/answer.txt`.

## Constraints

- `setup/answer.txt` must contain `"2"`.
- `setup/results.json` must have `counter=2`.
- `setup/processed.json` must contain both `task_001` and `task_002`.
- Counter must NOT be 3 (duplicate was correctly skipped).
