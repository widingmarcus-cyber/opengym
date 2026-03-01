# Step 2: Detect Configuration Drift

The configuration has been updated since your last session. The current config is now:

- **backup**: interval = "hourly" (unchanged)
- **sync**: interval = "weekly" (changed from "daily")

Compare the current configuration against the baseline you stored in `setup/drift_report.json` during Step 1.

Detect any drift and write your findings to `setup/answer.json` with:
- `"drifted"`: `true` if any field changed, `false` otherwise
- `"changes"`: array of objects describing each change, with keys `"task"`, `"field"`, `"from"` (baseline value), `"to"` (current value)

Also update `setup/config.json` to reflect the current (drifted) configuration state described above.
