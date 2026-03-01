# Challenge 205: Transaction Atomicity

## Difficulty: Hard
## Category: Failure Recovery

## Description

A configuration update script (`setup/config_updater.py`) writes to three config files simultaneously. If any write fails, all files should be left unchanged (atomic all-or-nothing). Currently the script writes directly to the target files, so a failure mid-way leaves the system in an inconsistent state.

The current broken state:
- `setup/config/database.json` — was partially overwritten (corrupted)
- `setup/config/cache.json` — was successfully overwritten (new values)
- `setup/config/api.json` — was NOT overwritten (still has old values)

Backup of original configs: `setup/backups/` (the state before the failed update)
The intended new values: `setup/intended_update.json`

Your job:
1. Restore all three config files to a consistent state (either ALL old or ALL new values).
2. Rewrite `setup/config_updater.py` to use atomic writes: write to temp files first, then rename all at once. If any step fails, roll back.
3. Run the rewritten updater to apply the intended update atomically.
4. Write `setup/transaction_log.json` documenting the atomic update.

## Expected Output

- `setup/config/database.json`, `setup/config/cache.json`, `setup/config/api.json` — all with the NEW intended values
- `setup/config_updater.py` — rewritten with atomic write pattern (write-to-temp + rename)
- `setup/transaction_log.json` — JSON with keys: `status` ("committed"), `files_updated` (list of 3 filenames), `atomic` (true), `method` ("write-tmp-rename")

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
