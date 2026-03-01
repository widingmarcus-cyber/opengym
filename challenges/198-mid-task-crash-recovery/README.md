# Challenge 198: Mid-Task Crash Recovery

## Difficulty: Hard
## Category: Failure Recovery

## Description

A data processing pipeline crashed mid-task while transforming records from `setup/input_records.json`. The crash log in `setup/crash_log.json` shows exactly where the process died and which records were already processed (saved in `setup/partial_output.json`).

Your job:
1. Read the crash log to determine which record the process crashed on and why.
2. Fix the bug in `setup/processor.py` that caused the crash.
3. Resume processing from where it left off (do NOT reprocess already-completed records).
4. Write the complete result to `setup/output.json` — it must contain all successfully processed records (both the ones from `partial_output.json` and the newly processed ones).
5. Write a recovery report to `setup/recovery_report.json` documenting what failed and how you recovered.

## Expected Output

- `setup/processor.py` — fixed version of the processor (the crash-causing bug must be resolved)
- `setup/output.json` — array of ALL processed records (partial + resumed), each with an added `"status": "processed"` field and a `"result"` field containing the transformed value
- `setup/recovery_report.json` — JSON object with keys: `crashed_on_record` (int), `crash_reason` (string), `records_recovered` (int), `total_records` (int)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
