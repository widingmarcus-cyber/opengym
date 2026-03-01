# Step 3: Process New Task

You are acting as the **Task Processor**.

You receive a new task:

```json
{"id": "task_002", "action": "increment_counter"}
```

**Your task:**

1. Read `setup/processed.json`. It contains `["task_001"]`.
2. Check if `task_002` is in the processed list. It is NOT, so process it.
3. Read `setup/results.json` (currently `{"counter": 1}`).
4. Increment the counter: `1 + 1 = 2`.
5. Write `{"counter": 2}` to `setup/results.json`.
6. Add `"task_002"` to `setup/processed.json`: `["task_001", "task_002"]`.
7. Write the final counter value to `setup/answer.txt`: `2`.

After this step:
- `setup/results.json` should be `{"counter": 2}`
- `setup/processed.json` should be `["task_001", "task_002"]`
- `setup/answer.txt` should contain `2`
