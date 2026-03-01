# Step 3: Generate Remediation Plan

## Task

Based on the drift report from Step 2, generate a remediation plan that will bring all servers back to baseline compliance.

1. Read `setup/drift_report.json` from Step 2.
2. For each drift, generate a remediation action that specifies what to change and what the target value should be.
3. Write `setup/remediation_plan.json`.

## Expected Output

`setup/remediation_plan.json`:
```json
{
  "total_remediations": <number>,
  "remediations": [
    {
      "server": "<server_name>",
      "field": "<field_path>",
      "action": "set",
      "target_value": <baseline_value>,
      "current_value": <drifted_value>
    },
    ...
  ]
}
```

## Notes

- There must be exactly one remediation for each drift detected in Step 2.
- `total_remediations` must equal `total_drifts` from the drift report.
- The `target_value` must always be the baseline value (we are restoring to baseline).
