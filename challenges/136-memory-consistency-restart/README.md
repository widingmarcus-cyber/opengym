# Challenge 136: Memory Consistency After Restart

**Difficulty:** Easy
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that your agent can initialize a state file, incrementally update it across sessions, and produce a consistent final state that reflects all accumulated changes.

## What This Tests

- Initializing persistent state correctly
- Reading, modifying, and writing back state across sessions
- Maintaining consistency of all fields through incremental updates

## Sessions

1. **Initialize State** -- Write the initial state `{"initialized": true, "count": 0, "items": []}` to `setup/state.json`.
2. **First Update** -- Read `setup/state.json`, increment `count` to 1, append `"apple"` to `items`, and write the updated state back.
3. **Second Update and Report** -- Read `setup/state.json`, increment `count` to 2, append `"banana"` to `items`, and write the final state to `setup/answer.json`.

## Constraints

- `setup/state.json` must reflect the final state: `{"initialized": true, "count": 2, "items": ["apple", "banana"]}`.
- `setup/answer.json` must contain the same final state.
