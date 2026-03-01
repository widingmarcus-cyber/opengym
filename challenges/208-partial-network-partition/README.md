# Challenge 208: Partial Network Partition

## Difficulty: Hard
## Category: Failure Recovery

## Description

A data synchronization script fetches data from 4 API endpoints (simulated as local JSON files). During a network partition, 2 of the 4 endpoints are "down" (their data files are corrupted/empty). The agent must:

1. Read `setup/endpoint_status.json` to learn which endpoints are up/down.
2. Read data from the working endpoints (`setup/endpoints/` directory).
3. Use cross-reference data in `setup/cross_references.json` to reconstruct the missing data from the working endpoints.
4. Produce a complete merged dataset in `setup/merged_data.json`.
5. Write `setup/partition_report.json` documenting the recovery.

The endpoints contain overlapping/related data, so the "down" endpoint data CAN be reconstructed from the "up" endpoints using the cross-references.

## Expected Output

- `setup/merged_data.json` — complete dataset with data from all 4 logical endpoints (reconstructed where necessary)
- `setup/partition_report.json` — JSON with keys: `endpoints_up` (list), `endpoints_down` (list), `records_from_live` (int), `records_reconstructed` (int), `total_records` (int)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
