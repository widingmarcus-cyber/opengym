# Challenge 188: Missed Schedule Catch-up

**Difficulty:** hard
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

A scheduled job was supposed to run every hour for hours 1 through 5, but some runs were missed. Your task is to analyze the schedule log, detect which runs were missed, and determine if catch-up execution is needed.

## Objectives

- Read `setup/schedule_log.json` which contains the scheduled and actual execution records.
- Identify which scheduled hours were missed (not executed).
- Write `setup/answer.json` with:
  - The list of missed hours
  - Whether catch-up is needed (true if any hours were missed)
  - Total number of scheduled runs
  - Total number of actually executed runs

## Expected Output

`setup/answer.json`:
```json
{
  "missed": [3, 4],
  "catch_up_needed": true,
  "total_scheduled": 5,
  "total_executed": 3
}
```
