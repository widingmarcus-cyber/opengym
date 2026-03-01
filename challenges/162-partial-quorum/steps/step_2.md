You are Node B in a distributed commit protocol. Your task is to cast your vote.

1. Read `setup/votes.json` (contains Node A's vote).
2. Add your vote while preserving Node A's entry. Write the updated file:

```json
{
  "node_a": {"vote": "commit", "timestamp": 1},
  "node_b": {"vote": "commit", "timestamp": 2}
}
```

IMPORTANT: You must preserve Node A's vote. Node C is unavailable and will not vote.
