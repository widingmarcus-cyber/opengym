# Step 1: Execute Subtasks

You are acting as the **Executor**.

Read `setup/subtasks.json`:

```json
[
  {"id": 1, "type": "compute", "input": 10},
  {"id": 2, "type": "compute", "input": 20},
  {"id": 3, "type": "compute", "input": -1},
  {"id": 4, "type": "compute", "input": 40},
  {"id": 5, "type": "compute", "input": 50}
]
```

Each `"compute"` task squares the input value. However, **negative inputs are invalid** and should result in a failure.

**Your task:** Process each subtask and write results to `setup/results.json`:

```json
[
  {"id": 1, "status": "success", "output": 100},
  {"id": 2, "status": "success", "output": 400},
  {"id": 3, "status": "failed", "output": null},
  {"id": 4, "status": "success", "output": 1600},
  {"id": 5, "status": "success", "output": 2500}
]
```

- Subtask 3 has input=-1, which is invalid. Mark it as `"failed"` with `"output": null`.
- All other subtasks should be `"success"` with the squared value as output.
