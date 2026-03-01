# Step 1: Initial Schedule Execution

Read `setup/schedule.json` which contains three tasks, each with an execution policy ("fresh" or "reuse").

Execute all tasks and record the results in `setup/execution_log.json`.

For each task execution, record:
- The task id
- The policy applied
- The run number (this is run 1)
- Whether a clean context was used ("fresh") or existing context was reused ("reuse")

Example format for `setup/execution_log.json`:
```json
{
  "runs": [
    {
      "run": 1,
      "executions": [
        {"id": "t1", "policy": "fresh", "context": "clean", "command": "initialize"},
        {"id": "t2", "policy": "reuse", "context": "new_initial", "command": "process"},
        {"id": "t3", "policy": "fresh", "context": "clean", "command": "cleanup"}
      ]
    }
  ]
}
```

Note: For "reuse" tasks on the first run, there is no prior context, so they start fresh but are marked as "new_initial" to indicate reuse policy was in effect.
