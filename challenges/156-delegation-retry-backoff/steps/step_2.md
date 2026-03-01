You are the Analyzer agent. Your task is to analyze the retry log from Step 1 and produce a summary.

1. Read `setup/retry_log.json`.
2. Determine:
   - The total number of attempts made.
   - The backoff pattern used (look at the `wait_seconds` values -- if they double each time, it's "exponential").
3. Write `setup/answer.json` with:
   - `"total_attempts"`: the number of entries in retry_log.json
   - `"backoff_pattern"`: `"exponential"` if the wait_seconds values double each time, otherwise `"linear"` or `"constant"`
