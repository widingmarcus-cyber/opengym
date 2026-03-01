# Challenge 131: Deleted Key Access

**Difficulty:** Medium
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Store a set of key-value pairs in persistent memory, then delete one key (because it has expired), and finally export only the remaining keys. This tests whether the agent can correctly mutate persisted state by removing a key and then accurately reflect the current state.

## What This Tests

- Ability to delete a specific key from a JSON data store
- Ensuring deleted data does not leak into subsequent outputs
- Accurate state reflection after mutation across sessions

## Sessions

1. **Store Initial Data** -- Write three key-value pairs to memory.json: name, role, and temp_token
2. **Delete Expired Key** -- Remove the "temp_token" key from memory.json (it has expired)
3. **Export Remaining Data** -- Write all remaining keys and values to answer.json as a flat dict. Must NOT include temp_token.

## Constraints

- After step 2, `setup/memory.json` must NOT contain "temp_token"
- `setup/answer.json` must contain "name" and "role" but NOT "temp_token"
