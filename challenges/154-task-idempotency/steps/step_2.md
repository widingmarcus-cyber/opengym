# Step 2: Handle Duplicate Task Delivery

You are acting as the **Task Processor**.

You receive this task again (duplicate delivery):

```json
{"id": "task_001", "action": "increment_counter"}
```

**Your task:**

1. Read `setup/processed.json`. It contains `["task_001"]`.
2. Check if `task_001` is already in the processed list. **It is!**
3. **Skip this task.** Do NOT increment the counter.
4. `setup/results.json` must remain `{"counter": 1}`.
5. `setup/processed.json` must remain `["task_001"]`.

**Important:** This tests idempotency. The same task delivered twice should only be processed once. The counter must NOT become 2 after this step.
