# Step 2: Second Schedule Execution and Summary

The schedule runs again. Execute all tasks from `setup/schedule.json` a second time.

- "fresh" policy tasks (t1, t3) must be re-executed from scratch with a clean context.
- "reuse" policy tasks (t2) should note they are reusing context from the previous run.

Update `setup/execution_log.json` to include both run 1 and run 2 executions.

Then write `setup/answer.json` with the total count of fresh vs reuse executions across both runs:
- `"fresh_count"`: total number of executions that used "fresh" policy across all runs
- `"reuse_count"`: total number of executions that used "reuse" policy across all runs
