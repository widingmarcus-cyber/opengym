# Challenge 226: Alert Deduplication

## Objective

Deduplicate repeated alerts by grouping them by root cause.

## Context

In production monitoring, a single incident often triggers the same alert many times. For example, a database going down might fire "DB connection failed" every 30 seconds for 10 minutes, plus related alerts from dependent services. Alert fatigue is a major problem in operations — deduplication is critical for incident response.

## Task

Read `setup/alerts.json` which contains an array of alert objects:

```json
{
  "alert_id": "a001",
  "timestamp": "2025-01-05T14:00:00Z",
  "severity": "critical",
  "source": "db-monitor",
  "title": "Database connection failed",
  "message": "Cannot connect to primary database on host db-master-01",
  "host": "db-master-01",
  "fingerprint": "db-conn-fail-db-master-01"
}
```

Write `setup/deduplicated.json` with alerts grouped by `fingerprint`. Each group should contain:

```json
{
  "fingerprint": "db-conn-fail-db-master-01",
  "title": "Database connection failed",
  "severity": "critical",
  "source": "db-monitor",
  "host": "db-master-01",
  "first_seen": "2025-01-05T14:00:00Z",
  "last_seen": "2025-01-05T14:05:00Z",
  "count": 11,
  "alert_ids": ["a001", "a003", "a005", ...]
}
```

## Requirements

- Group alerts by their `fingerprint` field
- For each group, record `first_seen` (earliest timestamp) and `last_seen` (latest timestamp)
- `count` is the number of alerts in the group
- `alert_ids` is a list of all alert IDs in the group, sorted chronologically
- `severity` should be the highest severity seen in the group (critical > high > medium > low)
- Output should be a JSON array of group objects, sorted by `first_seen` (ascending)
- The input has 20 alerts that should collapse to exactly 5 groups

## Verification

```bash
python3 tests/verify.py
```
