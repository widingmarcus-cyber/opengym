# Step 2: Second Schedule Execution and Summary

The schedule runs again. Execute all tasks from `setup/schedule.json` a second time.

- "fresh" policy tasks (t1, t3) must be re-executed from scratch with a clean context.
- "reuse" policy tasks (t2) should note they are reusing context from the previous run.

Update `setup/execution_log.json` to include both run 1 and run 2 executions.

Then write `setup/answer.json` with the total count of fresh vs reuse executions across both runs:
- t1 (fresh) ran in run 1 and run 2 = 2 fresh executions
- t2 (reuse) ran in run 1 and run 2 = 2 reuse executions
- t3 (fresh) ran in run 1 and run 2 = 2 fresh executions
- Total: fresh_count = 4, reuse_count = 2

Expected `setup/answer.json`:
```json
{"fresh_count": 4, "reuse_count": 2}
```
