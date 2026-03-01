# Step 2: Agent B Writes

You are acting as **Agent B**.

Read `setup/shared.json`. It already contains Agent A's data from the previous session.

**Your task:** Add Agent B's result to the shared file WITHOUT overwriting Agent A's data.

Add the following entry:

```json
{
  "agent_b": {
    "status": "done",
    "result": 99
  }
}
```

After this step, `setup/shared.json` must contain BOTH `agent_a` and `agent_b` entries:

```json
{
  "agent_a": {
    "status": "done",
    "result": 42
  },
  "agent_b": {
    "status": "done",
    "result": 99
  }
}
```

**Important:** Do NOT overwrite the file with only Agent B's data. You must merge both entries.
