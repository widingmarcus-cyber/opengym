# Challenge 227: Log Level Filtering

## Objective

Implement log level filtering to produce separate output files for each severity threshold.

## Context

Log levels follow a hierarchy: DEBUG < INFO < WARN < ERROR. When you set a minimum log level to WARN, you should see WARN and ERROR entries but not DEBUG or INFO. This is fundamental to observability — production systems typically run at INFO or WARN level, while debugging uses DEBUG.

## Task

Read `setup/app_logs.json` which contains an array of log entry objects:

```json
{
  "timestamp": "2025-01-05T14:00:01Z",
  "level": "INFO",
  "service": "user-service",
  "message": "Server started on port 8080"
}
```

Log levels have this hierarchy (lowest to highest): `DEBUG` < `INFO` < `WARN` < `ERROR`

Produce four filtered output files in the `setup/` directory:

- `setup/filter_debug.json` — all entries (DEBUG and above)
- `setup/filter_info.json` — INFO, WARN, and ERROR entries
- `setup/filter_warn.json` — WARN and ERROR entries only
- `setup/filter_error.json` — ERROR entries only

Each output file should contain a JSON array of the matching log entries, preserving their original order and all fields.

## Requirements

- Read all entries from `app_logs.json`
- Apply the level hierarchy correctly
- Preserve original entry order within each filtered output
- All four output files must be valid JSON arrays
- Entries must be unmodified (same fields and values as input)

## Verification

```bash
python3 tests/verify.py
```
