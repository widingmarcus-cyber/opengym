# Challenge 192: Retry Window Expiration

**Difficulty:** hard
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

When tasks fail, they can be retried -- but only within a defined retry window. Once the window expires, the task cannot be retried and must be marked as permanently failed.

Given the current time and a list of failed tasks with their retry windows, determine which tasks are still retryable and which have expired.

## Objectives

- Read `setup/failed_tasks.json` which contains failed tasks with timestamps and retry windows.
- Read `setup/current_time.txt` which contains the current time.
- For each task, calculate elapsed time since failure and compare against the retry window.
- Write `setup/answer.json` with lists of retryable and expired tasks.

## Data

Current time: `2024-01-01T00:30:00Z`

Tasks:
- t1: failed at 00:00, retry window 60 min -> 30 min elapsed < 60 min -> retryable
- t2: failed at 00:00, retry window 10 min -> 30 min elapsed > 10 min -> expired
- t3: failed at 00:25, retry window 60 min -> 5 min elapsed < 60 min -> retryable

## Expected Output

`setup/answer.json`:
```json
{
  "retryable": ["t1", "t3"],
  "expired": ["t2"]
}
```
