You are the Executor agent. Your task is to execute a task that simulates transient failures with exponential backoff retries.

The task logic:
1. Read `setup/attempt_counter.txt` to get the current attempt count (starts at 0).
2. For each attempt:
   a. Increment the counter by 1 and write it back to `setup/attempt_counter.txt`.
   b. If the counter is less than 3, the task "fails". Write "FAILED" to `setup/result.txt`.
   c. If the counter is 3 or greater, the task "succeeds". Write "SUCCESS" to `setup/result.txt`.
3. Log each attempt to `setup/retry_log.json` as a JSON array. Each entry should have:
   - `"attempt"`: the attempt number (1, 2, 3, ...)
   - `"status"`: `"failed"` or `"success"`
   - `"wait_seconds"`: the backoff wait before next retry. Use exponential backoff: 1, 2, 4, 8, ... For the successful attempt (no retry needed), use 0.

Example retry_log.json:
```json
[
  {"attempt": 1, "status": "failed", "wait_seconds": 1},
  {"attempt": 2, "status": "failed", "wait_seconds": 2},
  {"attempt": 3, "status": "success", "wait_seconds": 0}
]
```

You must simulate all 3 attempts in this single step. The final state of `setup/result.txt` should be "SUCCESS" and `setup/attempt_counter.txt` should be "3".
