# Step 1: Agent A Claims Tasks

You are acting as **Agent A**.

Read `setup/tasks.json` to see the available tasks:

```json
[
  {"id": 1, "name": "build"},
  {"id": 2, "name": "test"},
  {"id": 3, "name": "lint"},
  {"id": 4, "name": "deploy"},
  {"id": 5, "name": "monitor"}
]
```

**Your task:** Claim tasks 1, 2, and 3. Write them to `setup/task_registry.json` under the key `"agent_a"`:

```json
{
  "agent_a": [1, 2, 3]
}
```

The file must be valid JSON after this step.
