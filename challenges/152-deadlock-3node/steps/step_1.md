# Step 1: Detect the 3-Node Cycle

You are acting as the **Detector**.

Read `setup/graph.json`. It describes a dependency graph where each node specifies which other node it waits for.

**Your task:** Analyze the graph to detect a cycle. Walk the dependency chain from any starting node and determine if it loops back.

Write your findings to `setup/resolution.json` as a JSON object with:

- `"cycle"`: array — the ordered list of nodes forming the cycle (include the starting node again at the end to show the loop). The cycle should have length N+1 for N nodes involved.
- `"break_at"`: string — the node whose dependency will be broken to resolve the deadlock. You may choose any node in the cycle.
