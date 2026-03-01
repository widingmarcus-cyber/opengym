# Step 1: Read Baseline Configuration

## Task

Read `setup/baseline_config.json` and create a snapshot file.

1. Read the baseline configuration for all 5 servers.
2. Write `setup/baseline_snapshot.json` containing the full configuration keyed by server name, plus a `server_count` field and a `timestamp` field (use "2024-01-15T00:00:00Z").

## Expected Output

`setup/baseline_snapshot.json`:
```json
{
  "timestamp": "2024-01-15T00:00:00Z",
  "server_count": 5,
  "servers": {
    "web-01": { ... },
    "web-02": { ... },
    ...
  }
}
```
