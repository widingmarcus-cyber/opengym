# Challenge 137: Concurrent Memory Writes

**Difficulty:** Hard
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that your agent can handle multiple agents writing to a shared memory file without overwriting each other's data, and then aggregate results from all agents.

## What This Tests

- Writing to shared persistent storage without overwriting existing data
- Merging contributions from multiple agents into a single JSON structure
- Correctly aggregating values from a shared state file

## Sessions

1. **Agent A Writes** -- Write Agent A's result `{"agent_a": {"status": "done", "result": 42}}` to `setup/shared.json`.
2. **Agent B Writes** -- Read `setup/shared.json`, then ADD Agent B's result `{"agent_b": {"status": "done", "result": 99}}` WITHOUT overwriting Agent A's data. Both entries must coexist.
3. **Coordinator Aggregates** -- Read `setup/shared.json`, sum the results from both agents (42 + 99 = 141), and write `{"total": 141}` to `setup/answer.json`.

## Constraints

- `setup/shared.json` must contain BOTH `agent_a` and `agent_b` entries after step 2.
- `setup/answer.json` must contain `{"total": 141}`.
- Agent B must NOT overwrite Agent A's data in step 2.
