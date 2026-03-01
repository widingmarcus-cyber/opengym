# Step 2: Agent B Claims Remaining Tasks

You are acting as **Agent B**.

Read `setup/task_registry.json` to see which tasks are already claimed by Agent A.

**Your task:** Claim the remaining unclaimed tasks under the key `"agent_b"`. You must NOT claim any task that is already assigned to Agent A.

After reading the registry, you should find that tasks 1, 2, 3 are already claimed. Claim tasks 4 and 5:

```json
{
  "agent_a": [1, 2, 3],
  "agent_b": [4, 5]
}
```

**Important:** Do NOT overwrite Agent A's entries. Do NOT claim any task ID that already appears under `agent_a`.
