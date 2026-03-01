# Challenge 129: Versioned Memory Retrieval

**Difficulty:** Medium
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (2 steps)

## Objective

Store multiple versioned entries for a configuration key in persistent memory, then retrieve a specific version by number when asked. This tests whether the agent can maintain and query a versioned data structure across sessions.

## What This Tests

- Ability to store structured, versioned data in JSON
- Correct retrieval of a specific version from a list of entries
- Persistence and data integrity across sessions

## Sessions

1. **Store Versions** -- Write 3 versioned entries for the key "config" to memory.json (version 1 = "alpha", version 2 = "beta", version 3 = "gamma")
2. **Retrieve by Version** -- Read the task, which asks for the value of "config" at version 2. Write the value to answer.txt.

## Constraints

- `setup/memory.json` must contain all 3 versioned entries
- `setup/answer.txt` must contain exactly the string "beta"
