# Challenge 148: File Write Race

**Difficulty:** Medium
**Category:** shared-resources
**Dimension:** multi-agent
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that multiple agents can write to a shared JSON file without overwriting each other's data, and then verify the merged result.

## What This Tests

- Safe concurrent writes to a shared file
- Merging data from multiple agents into a single JSON structure
- Verifying data integrity after multi-agent writes

## Sessions

1. **Agent A Writes** -- Write `{"agent_a_data": [1, 2, 3]}` to `setup/output.json` under the key `"agent_a"`.
2. **Agent B Writes** -- Read `setup/output.json`, ADD `{"agent_b_data": [4, 5, 6]}` under the key `"agent_b"` WITHOUT overwriting `agent_a`.
3. **Merger Verifies** -- Verify both entries exist. Write `setup/answer.json` with `{"merged": true, "total_items": 6}`.

## Constraints

- `setup/output.json` must contain BOTH `agent_a` and `agent_b` entries after step 2.
- Agent B must NOT overwrite Agent A's data in step 2.
- `setup/answer.json` must contain `{"merged": true, "total_items": 6}`.
