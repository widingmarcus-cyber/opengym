# Step 1: Detect the 3-Node Cycle

You are acting as the **Detector**.

Read `setup/graph.json`. It contains:

```json
{
  "A": {"waits_for": "B"},
  "B": {"waits_for": "C"},
  "C": {"waits_for": "A"}
}
```

This describes a circular dependency among three nodes:
- A waits for B
- B waits for C
- C waits for A
- This forms the cycle: A -> B -> C -> A

**Your task:** Detect the cycle and write a resolution plan to `setup/resolution.json`:

```json
{
  "cycle": ["A", "B", "C", "A"],
  "break_at": "A"
}
```

The `break_at` field indicates which node's dependency will be broken to resolve the deadlock. You may choose any node in the cycle.
