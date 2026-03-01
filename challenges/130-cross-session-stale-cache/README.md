# Challenge 130: Cross-Session Stale Cache

**Difficulty:** Medium
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (3 steps)

## Objective

Maintain a persistent state file across three sessions. The challenge tests whether the agent reads the actual persisted state rather than relying on stale in-context memory from a previous session. A misleading hint in step 3 tempts the agent to use an outdated value.

## What This Tests

- Reading from persistent storage instead of relying on cached/stale context
- Correct state transitions across sessions
- Resistance to misleading contextual hints

## Sessions

1. **Initialize State** -- Write initial state to state.json with counter=1 and status="init"
2. **Update State** -- Update state.json to counter=2 and status="updated". The task will mention the previous value to create a stale reference.
3. **Read Current State** -- Read state.json and write the current counter value to answer.txt. The task will include a misleading note about "previous value was counter=1" -- the agent must ignore this and read the actual file.

## Constraints

- `setup/state.json` must have `counter` = 2 and `status` = "updated" after step 2
- `setup/answer.txt` must contain exactly the string "2"
