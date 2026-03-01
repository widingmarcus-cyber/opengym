# Challenge 199: OOM Simulation

## Difficulty: Hard
## Category: Failure Recovery

## Description

A data aggregation script (`setup/aggregator.py`) loads an entire large dataset into memory at once, causing an out-of-memory crash. The crash report is in `setup/oom_report.json`.

The dataset is in `setup/data_chunks/` — 5 JSON files, each containing 1000 records. The original aggregator tried to load all 5000 records into a single list, sort them, compute statistics, and write a summary.

Your job:
1. Rewrite `setup/aggregator.py` to use a memory-efficient streaming/chunked approach that processes one chunk at a time without loading all data into memory simultaneously.
2. The rewritten aggregator must produce `setup/summary.json` with these fields:
   - `total_records` (int): total number of records across all chunks
   - `sum_value` (float): sum of all `value` fields
   - `avg_value` (float): average of all `value` fields (rounded to 2 decimal places)
   - `max_value` (float): maximum `value`
   - `min_value` (float): minimum `value`
   - `processing_method` (string): must be `"chunked"` (not `"bulk"`)
3. Run the rewritten aggregator to produce the summary.

## Expected Output

- `setup/aggregator.py` — rewritten with chunked/streaming processing
- `setup/summary.json` — aggregation results

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
