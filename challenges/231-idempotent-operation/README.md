# Challenge 231: Idempotent Operation

## Objective

Fix a data processing script so that running it multiple times produces the same result as running it once.

## Context

Idempotency means that performing an operation multiple times has the same effect as performing it once. This is critical in distributed systems — if a message is delivered twice, or a job is retried after a timeout, the system should not produce duplicate or corrupted data. Common idempotency bugs include appending instead of upserting, missing deduplication, and accumulating side effects.

## Task

Read `setup/process.py` which processes records from `setup/input_records.json` and writes results to `setup/output.json`. The script has multiple idempotency bugs:

1. **Append bug**: It appends to the output file instead of replacing, so running it twice doubles the data
2. **Counter bug**: It increments a persistent counter in `setup/state.json` on every run, so the "processed_count" grows with each run
3. **Duplicate bug**: If the input has records with the same `id`, it processes all of them instead of deduplicating by `id`

Fix `setup/process.py` so that:

- Running `python3 setup/process.py` any number of times produces the exact same `setup/output.json`
- `setup/state.json` has the same content after 1 run or 5 runs
- Duplicate input records (same `id`) are processed only once (keep the first occurrence)

## Requirements

- Fix ALL three idempotency bugs
- Output must be written atomically (overwrite, not append)
- State file must reflect the actual processed data, not accumulate across runs
- Input records with duplicate `id` fields should be deduplicated (keep first occurrence)
- Do NOT modify `setup/input_records.json`

## Verification

```bash
python3 tests/verify.py
```
