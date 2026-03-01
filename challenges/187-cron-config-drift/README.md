# Challenge 187: Cron Config Drift

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** multi-session (2 steps)

## Description

Configuration drift occurs when a system's actual configuration diverges from its intended baseline over time. In this challenge, you manage a scheduled task configuration and must detect when drift has occurred.

## Objectives

### Step 1
- Read `setup/config.json` which contains the current task schedule.
- Record the current configuration as a "baseline" snapshot in `setup/drift_report.json`.

### Step 2
- The configuration has drifted. The current config is now: backup=hourly, sync=weekly (sync changed from "daily" to "weekly").
- Compare the current configuration against the baseline stored in `setup/drift_report.json`.
- Detect and report the drift.
- Write `setup/answer.json` with drift detection results.

## Expected Output

`setup/answer.json`:
```json
{
  "drifted": true,
  "changes": [
    {"task": "sync", "field": "interval", "from": "daily", "to": "weekly"}
  ]
}
```
