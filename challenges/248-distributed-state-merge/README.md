# Challenge 248: Distributed State Merge with Conflict Resolution

## Scenario

Three agents (Alpha, Beta, Gamma) each write key-value entries to a shared state file across three separate sessions. In a fourth session, a coordinator merges the results and produces a final report.

Each agent reads from its own partition file and writes entries to `setup/shared_state.json`. Entries follow this format:

```json
{
  "key_name": {
    "value": "some_value",
    "agent": "alpha",
    "timestamp": "2024-01-15T10:00:00",
    "version": 1
  }
}
```

## Conflict Resolution Rules

When multiple agents write the same key, conflicts are resolved using a three-tier system:

1. **Latest timestamp wins** — the entry with the most recent timestamp takes precedence.
2. **Highest version wins** — if timestamps are identical, the entry with the higher version number wins.
3. **Alphabetical agent name wins** — if both timestamp and version are identical, the agent whose name comes first alphabetically wins (e.g., "alpha" beats "beta").

## Sessions

- **Session 1**: Agent-Alpha reads `setup/partitions/partition_a.json` and writes to `setup/shared_state.json`.
- **Session 2**: Agent-Beta reads `setup/partitions/partition_b.json` and writes/updates `setup/shared_state.json`.
- **Session 3**: Agent-Gamma reads `setup/partitions/partition_c.json` and writes/updates `setup/shared_state.json`.
- **Session 4**: Coordinator reads `setup/shared_state.json` and writes `setup/merge_result.json`.

## Expected Output

`setup/merge_result.json` must contain:

```json
{
  "entries": {
    "key": {
      "value": "...",
      "winner_agent": "...",
      "timestamp": "...",
      "version": 1
    }
  },
  "stats": {
    "total_keys": 18,
    "alpha_wins": 5,
    "beta_wins": 5,
    "gamma_wins": 8
  },
  "conflict_log": [
    {
      "key": "...",
      "agents_involved": ["alpha", "beta"],
      "winner": "alpha"
    }
  ]
}
```

The `conflict_log` should only include entries where multiple agents wrote the same key. Each conflict entry lists all agents that wrote that key (sorted alphabetically) and identifies the winner.

## Partition Details

- **Partition A** (Alpha): 8 entries — `db_host`, `db_port`, `cache_ttl`, `log_level`, `max_retries`, `timeout`, `api_key`, `region`
- **Partition B** (Beta): 8 entries — `db_host`, `cache_ttl`, `log_level`, `timeout`, `batch_size`, `queue_url`, `worker_count`, `retry_delay`
- **Partition C** (Gamma): 8 entries — `max_retries`, `batch_size`, `shard_count`, `replica_count`, `health_check_interval`, `backup_schedule`, `compression_algo`, `encryption_key_id`

There are 6 conflicting keys across partitions. The remaining 12 keys are unique to a single agent.
