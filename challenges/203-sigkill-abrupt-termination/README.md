# Challenge 203: SIGKILL Abrupt Termination

## Difficulty: Hard
## Category: Failure Recovery

## Description

A database migration script was killed with SIGKILL (kill -9) while writing records. Unlike SIGTERM, SIGKILL cannot be caught — the process died instantly, leaving behind:

- `setup/db_before.json` — the original database state (20 records)
- `setup/db_partial.json` — the corrupted database (some records updated, some half-written, some missing fields)
- `setup/migration_plan.json` — the intended migration (describes all changes that should have been applied)
- `setup/write_log.json` — partial write log showing which writes were attempted before the kill

Your job:
1. Analyze the partial state to determine which records were successfully migrated, which were corrupted, and which were not yet touched.
2. Reconstruct a clean database by:
   - Keeping successfully migrated records as-is
   - Fixing corrupted records (apply the migration properly)
   - Applying the migration to untouched records
3. Write the repaired database to `setup/db_repaired.json`
4. Write a damage report to `setup/damage_report.json`

## Expected Output

- `setup/db_repaired.json` — array of 20 fully-migrated records, each with fields: `id`, `name`, `email`, `role`, `version` (must be 2)
- `setup/damage_report.json` — JSON with keys: `total_records` (20), `clean_records` (int), `corrupted_records` (int), `untouched_records` (int), `all_repaired` (true)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
