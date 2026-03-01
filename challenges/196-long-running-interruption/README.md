# Challenge 196: Long-Running Interruption

**Difficulty:** hard
**Category:** task-sequencing
**Dimension:** planning
**Type:** multi-session (2 steps)

## Description

A long-running job processes items 1 through 10 sequentially. During the first session, the job is interrupted after processing item 7. In the second session, the job must resume from where it left off and complete the remaining items.

This tests an agent's ability to persist progress state and resume interrupted work.

## Objectives

### Step 1
- Process items 1 through 10, but an interruption occurs after item 7.
- Write progress to `setup/progress.json` recording which items were completed, which remain, and that an interruption occurred.

### Step 2
- Read `setup/progress.json` to determine where processing left off.
- Resume processing from item 8 and complete items 8, 9, 10.
- Update `setup/progress.json` to reflect full completion.
- Write `setup/answer.json` with summary.

## Expected Output

`setup/progress.json` (after step 2):
```json
{
  "completed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "remaining": [],
  "interrupted": false
}
```

`setup/answer.json`:
```json
{
  "total_completed": 10,
  "resumed_from": 8
}
```
