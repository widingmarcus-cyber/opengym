# Challenge 197: Cron Idempotency

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** multi-session (2 steps)

## Description

Idempotency is a critical property for scheduled tasks: running the same task multiple times should produce the same result as running it once. A "daily_report" task should only actually execute once per day, even if triggered multiple times.

Your job is to implement idempotent task execution across two sessions.

## Objectives

### Step 1
- Run the "daily_report" task for the first time.
- Write `setup/state.json`: `{"report_generated": true, "run_count": 1}`
- Log the run in `setup/run_log.json`.

### Step 2
- The "daily_report" task is triggered again (simulating a double-trigger or retry).
- Check `setup/state.json` -- the report was already generated today.
- Since the task is idempotent, do NOT execute it again. The run_count stays at 1.
- Write `setup/answer.json`: `{"idempotent": true, "actual_runs": 1}`

## Expected Output

`setup/state.json` (must NOT be incremented to 2):
```json
{"report_generated": true, "run_count": 1}
```

`setup/answer.json`:
```json
{"idempotent": true, "actual_runs": 1}
```
