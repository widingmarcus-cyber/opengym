# Step 2: Agent B Writes

You are acting as **Agent B**.

Read `setup/output.json`. It already contains Agent A's data from the previous session.

**Your task:** Add Agent B's data to the file WITHOUT overwriting Agent A's data.

Add the following entry under the key `"agent_b"`:

```json
{
  "agent_b": {
    "agent_b_data": [4, 5, 6]
  }
}
```

After this step, `setup/output.json` must contain BOTH `agent_a` and `agent_b` entries.

**Important:** Do NOT overwrite the file with only Agent B's data. You must merge both entries.
