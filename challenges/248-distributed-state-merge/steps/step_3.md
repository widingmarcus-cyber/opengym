# Step 3: Agent-Gamma Writes

You are Agent-Gamma. Read `setup/partitions/partition_c.json`. For each entry, write or update `setup/shared_state.json` using the following format:

```json
{
  "key_name": {
    "value": "<entry value>",
    "agent": "gamma",
    "timestamp": "<entry timestamp>",
    "version": <entry version>
  }
}
```

If `setup/shared_state.json` already has the key, apply the conflict resolution rules described in the README:

1. Latest timestamp wins.
2. For timestamp ties, highest version wins.
3. For version ties, alphabetically first agent name wins.

Only overwrite an existing entry if you (gamma) win the conflict. Preserve all other existing entries.
