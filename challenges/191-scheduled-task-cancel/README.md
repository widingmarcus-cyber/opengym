# Challenge 191: Scheduled Task Cancellation

**Difficulty:** easy
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

You have a task queue with several pending tasks. Some tasks have been cancelled and should not be executed. Process the queue, execute only non-cancelled tasks, and produce a report.

## Objectives

- Read `setup/queue.json` which contains a task queue.
- Execute only tasks with status "pending" (skip "cancelled" ones).
- Write `setup/results.json` with execution results for all tasks.
- Write `setup/answer.txt` with the count of tasks that were actually executed.

## Expected Output

`setup/results.json`:
```json
[
  {"id": 1, "executed": true},
  {"id": 2, "executed": true},
  {"id": 3, "executed": false, "reason": "cancelled"},
  {"id": 4, "executed": true}
]
```

`setup/answer.txt`:
```
3
```
