# Step 1: Record Configuration Baseline

Read `setup/config.json` which contains the current task schedule configuration:

```json
{
  "tasks": [
    {"name": "backup", "interval": "hourly"},
    {"name": "sync", "interval": "daily"}
  ]
}
```

Record this as the "baseline" configuration in `setup/drift_report.json`.

Example format for `setup/drift_report.json`:
```json
{
  "baseline": {
    "tasks": [
      {"name": "backup", "interval": "hourly"},
      {"name": "sync", "interval": "daily"}
    ]
  },
  "recorded_at": "step_1"
}
```
