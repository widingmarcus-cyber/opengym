# Step 2: Detect Configuration Drift

The configuration has been updated since your last session. The current config is now:

- **backup**: interval = "hourly" (unchanged)
- **sync**: interval = "weekly" (changed from "daily")

Compare the current configuration against the baseline you stored in `setup/drift_report.json` during Step 1.

Detect the drift and write your findings to `setup/answer.json`:

```json
{
  "drifted": true,
  "changes": [
    {"task": "sync", "field": "interval", "from": "daily", "to": "weekly"}
  ]
}
```

Also update `setup/config.json` to reflect the current (drifted) state:
```json
{
  "tasks": [
    {"name": "backup", "interval": "hourly"},
    {"name": "sync", "interval": "weekly"}
  ]
}
```
