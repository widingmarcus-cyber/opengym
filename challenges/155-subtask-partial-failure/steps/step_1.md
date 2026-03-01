# Step 1: Execute Subtasks

You are acting as the **Executor**.

Read `setup/subtasks.json`. It contains a list of subtasks, each with an `"id"`, `"type"`, and `"input"` value.

For `"compute"` type tasks, the operation is to **square** the input value. However, **negative inputs are invalid** and should result in a failure.

**Your task:** Process each subtask and write results to `setup/results.json` as a JSON array. Each entry must have:
- `"id"`: the subtask ID
- `"status"`: `"success"` or `"failed"`
- `"output"`: the computed value (squared input), or `null` if failed

Rules:
- Negative inputs are invalid and should be marked as `"failed"` with `"output": null`.
- All other subtasks should be `"success"` with the squared value as output.
