# Step 1: Detect the Deadlock

You are acting as the **Detector**.

Read `setup/dependencies.json`. It describes which agents are waiting for output from other agents.

**Your task:** Analyze the dependency graph for cycles. If a circular dependency exists (Agent X waits for Agent Y, and Agent Y waits for Agent X), that is a **deadlock**.

Write your findings to `setup/resolution.json` as a JSON object with the following fields:

- `"cycle_detected"`: boolean — whether a cycle was found
- `"cycle"`: array — the ordered list of nodes in the cycle (include the starting node again at the end to show the loop)
- `"resolution"`: string — a description of how to break the cycle (which agent should produce a default output)

You must programmatically detect the cycle from the dependency data, not assume a specific graph structure.
