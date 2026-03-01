# Step 3: Coordinator Aggregates

You are acting as the **Coordinator**.

Read `setup/shared.json`, which contains results from both Agent A and Agent B.

1. Extract the `result` value from `agent_a` (should be 42)
2. Extract the `result` value from `agent_b` (should be 99)
3. Compute the total: 42 + 99 = 141

Write the aggregated result to `setup/answer.json`:

```json
{
  "total": 141
}
```
