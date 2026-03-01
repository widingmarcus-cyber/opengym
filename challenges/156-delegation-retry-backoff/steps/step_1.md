You are the Executor agent. Your task is to execute a task that simulates transient failures with exponential backoff retries.

The task logic:
1. Read `setup/attempt_counter.txt` to get the current attempt count (starts at 0).
2. Simulate multiple attempts. For each attempt:
   a. Increment the counter by 1 and write it back to `setup/attempt_counter.txt`.
   b. If the counter is less than 3, the task "fails". Write "FAILED" to `setup/result.txt`.
   c. If the counter reaches 3 or more, the task "succeeds". Write "SUCCESS" to `setup/result.txt`.
3. Log each attempt to `setup/retry_log.json` as a JSON array. Each entry should have:
   - `"attempt"`: the attempt number (starting from 1)
   - `"status"`: `"failed"` or `"success"`
   - `"wait_seconds"`: the backoff wait before the next retry. Use **exponential backoff** (each wait should be greater than the previous). For the final successful attempt (no retry needed), use 0.

You must simulate all attempts in this single step. The final state of `setup/result.txt` should reflect the outcome of the last attempt.
