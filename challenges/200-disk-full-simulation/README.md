# Challenge 200: Disk Full Simulation

## Difficulty: Medium
## Category: Failure Recovery

## Description

A file-processing script failed because the disk was "full." The simulation uses a quota system: the `setup/quota.json` file defines a maximum total file size for the `setup/workspace/` directory. The workspace currently contains temp files, partial outputs, and cache files that exceed the quota.

Your job:
1. Read `setup/quota.json` to understand the size constraint.
2. Examine `setup/workspace/` — it contains temp files (`*.tmp`), cache files (`*.cache`), partial outputs (`*.partial`), and the important input file `data.csv`.
3. Clean up unnecessary files (temp, cache, partial) to bring the workspace under quota.
4. Run the writer script `setup/writer.py` which reads `data.csv` and writes `result.csv` — but only if there is enough space (it checks quota).
5. Produce `setup/cleanup_report.json` documenting which files were removed and how much space was freed.

## Rules

- Do NOT delete `data.csv` — it is the input
- Do NOT delete `quota.json` — it defines the constraints
- The final workspace size (all files combined) must be under the quota
- `result.csv` must be present and contain the processed output

## Expected Output

- `setup/workspace/result.csv` — processed output from writer.py
- `setup/cleanup_report.json` — JSON with keys: `files_removed` (list of filenames), `bytes_freed` (int), `final_size_bytes` (int), `quota_bytes` (int)
- No temp/cache/partial files remaining in workspace

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
