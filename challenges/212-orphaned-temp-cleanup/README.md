# Challenge 212: Orphaned Temp Cleanup

## Difficulty: Medium
## Category: Failure Recovery

## Description

A temp directory (`setup/tempdir/`) contains a mix of active and orphaned temporary files. Orphaned files are left behind from crashed processes. Active files are still in use by running processes.

Your job:
1. Read `setup/active_locks.json` — lists lock files that indicate ACTIVE processes (do NOT delete these or their associated temp files).
2. Examine `setup/tempdir/` — contains `.tmp` data files and `.lock` lock files.
3. The convention: each temp file `<name>.tmp` has a corresponding lock file `<name>.lock` if its process is still running. If the lock file is missing OR is listed in `setup/stale_indicators.json`, the temp file is orphaned.
4. Read `setup/stale_indicators.json` — lists lock files that exist on disk but belong to crashed processes (stale locks).
5. Delete all orphaned temp files AND stale lock files.
6. Leave active temp files and their lock files untouched.
7. Write `setup/cleanup_manifest.json` documenting what was removed.

## Rules

- A temp file is ACTIVE if its corresponding lock file exists AND is listed in `active_locks.json`
- A temp file is ORPHANED if it has no lock file OR its lock file is listed in `stale_indicators.json`
- Stale lock files (in stale_indicators.json) should also be deleted
- NEVER delete active lock files or active temp files

## Expected Output

- Orphaned temp files and stale locks removed from `setup/tempdir/`
- Active files untouched
- `setup/cleanup_manifest.json` — JSON with keys: `orphaned_temps_removed` (list of filenames), `stale_locks_removed` (list of filenames), `active_files_kept` (list of filenames), `total_removed` (int), `total_kept` (int)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
