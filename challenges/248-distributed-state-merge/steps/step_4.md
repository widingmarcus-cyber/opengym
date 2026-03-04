# Step 4: Coordinator Merges

You are the Coordinator. Read `setup/shared_state.json` and write `setup/merge_result.json` containing the final merged result.

The output format must be:

```json
{
  "entries": {
    "key_name": {
      "value": "...",
      "winner_agent": "...",
      "timestamp": "...",
      "version": 1
    }
  },
  "stats": {
    "total_keys": 18,
    "alpha_wins": 6,
    "beta_wins": 6,
    "gamma_wins": 6
  },
  "conflict_log": [
    {
      "key": "db_host",
      "agents_involved": ["alpha", "beta"],
      "winner": "beta"
    }
  ]
}
```

Rules:
- `entries` contains every key from shared_state.json with its winning value, winner_agent, timestamp, and version.
- `stats.total_keys` is the total number of unique keys.
- `stats.alpha_wins`, `beta_wins`, `gamma_wins` count how many keys each agent won.
- `conflict_log` lists ONLY keys where multiple agents wrote the same key. Each entry includes the key name, a sorted list of agents_involved, and the winner agent name.
