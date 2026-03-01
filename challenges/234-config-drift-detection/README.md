# Challenge 234: Config Drift Detection

## Objective

Manage infrastructure configuration across multiple sessions. You must detect configuration drift between a known baseline and a current state, then produce a remediation plan to bring the infrastructure back into compliance.

This is a **multi-session challenge** with 3 steps. See the `steps/` directory for per-step instructions.

## Setup

- `setup/baseline_config.json` - The known-good baseline configuration for 5 servers.
- `setup/current_config.json` - The current (potentially drifted) configuration. Initially identical to baseline.

## Overall Flow

1. **Step 1**: Read and acknowledge the baseline configuration. Write `setup/baseline_snapshot.json`.
2. **Step 2**: The current config has drifted. Detect all differences and write `setup/drift_report.json`.
3. **Step 3**: Generate a remediation plan to fix all detected drifts. Write `setup/remediation_plan.json`.

## Constraints

- Each step builds on the results of the previous step.
- Drift detection must be exact (field-level comparison).
- The remediation plan must address every detected drift.
