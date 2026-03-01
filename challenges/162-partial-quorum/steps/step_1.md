You are Node A in a distributed commit protocol. Your task is to cast your vote.

Write your vote to `setup/votes.json`:

```json
{
  "node_a": {"vote": "commit", "timestamp": 1}
}
```

You are the first node to vote, so create the file fresh. Node B will add their vote in the next step. Node C is unavailable and will not vote.
