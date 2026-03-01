You are the Coordinator. Your task is to evaluate whether quorum has been reached and make a commit/abort decision.

1. Read `setup/votes.json` (contains votes from Node A and Node B).
2. Count the votes. There are 3 total nodes (A, B, C). Quorum requires a majority: at least 2 out of 3 nodes.
3. Determine:
   - How many votes were received
   - How many votes are needed for quorum (2)
   - Whether quorum was reached
   - The decision: "commit" if quorum reached and all votes are "commit", otherwise "abort"
4. Write `setup/answer.json`:

```json
{
  "quorum_reached": true,
  "votes_received": 2,
  "votes_needed": 2,
  "decision": "commit"
}
```
