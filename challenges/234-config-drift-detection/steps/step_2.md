# Step 2: Detect Configuration Drift

## Task

The current configuration has drifted from the baseline. Compare `setup/current_config.json` against `setup/baseline_config.json` and identify all differences.

1. Compare every field of every server between baseline and current.
2. Write `setup/drift_report.json` listing each drift found.

## Expected Output

`setup/drift_report.json`:
```json
{
  "total_drifts": <number>,
  "drifts": [
    {
      "server": "<server_name>",
      "field": "<field_path>",
      "baseline_value": <value>,
      "current_value": <value>
    },
    ...
  ]
}
```

## Notes

- Compare all nested fields. Use dot notation for nested paths (e.g., "firewall.ssh_enabled").
- A drift is any field whose value differs between baseline and current.
- Missing or added fields also count as drifts.
