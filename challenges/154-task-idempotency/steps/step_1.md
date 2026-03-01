# Step 1: Process First Task

You are acting as the **Task Processor**.

You receive this task:

```json
{"id": "task_001", "action": "increment_counter"}
```

**Your task:**

1. Read `setup/results.json` (currently `{"counter": 0}`).
2. Read `setup/processed.json` (currently `[]`).
3. Check if `task_001` is in the processed list. It is not, so process it.
4. Increment the counter: `0 + 1 = 1`.
5. Write `{"counter": 1}` to `setup/results.json`.
6. Add `"task_001"` to `setup/processed.json`: `["task_001"]`.

After this step:
- `setup/results.json` should be `{"counter": 1}`
- `setup/processed.json` should be `["task_001"]`
