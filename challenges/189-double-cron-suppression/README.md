# Challenge 189: Double Cron Suppression

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** single-session

## Description

A cron scheduler has a bug that sometimes triggers the same task twice at the same time slot. Your task is to detect and suppress these duplicate triggers, keeping only the first trigger per time slot.

## Objectives

- Read `setup/trigger_log.json` which contains task trigger records, some of which are duplicates.
- Deduplicate the triggers: keep only the first trigger for each time slot.
- Write `setup/answer.json` with the deduplicated list and a count of how many duplicates were removed.

## Expected Output

`setup/answer.json`:
```json
{
  "deduplicated": [
    {"task": "report", "triggered_at": "10:00", "id": "run_1"},
    {"task": "report", "triggered_at": "11:00", "id": "run_3"}
  ],
  "duplicates_removed": 1
}
```
