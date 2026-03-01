# Challenge 149: Distributed Lock

**Difficulty:** Hard
**Category:** shared-resources
**Dimension:** multi-agent
**Type:** Multi-session (3 steps)

## Objective

Demonstrate that agents can safely coordinate access to a shared resource using a lock file, ensuring mutual exclusion and proper lock release.

## What This Tests

- Acquiring and releasing a distributed lock
- Writing to a shared resource while holding a lock
- Proper lock lifecycle: check -> acquire -> operate -> release
- Multiple agents accessing the same resource sequentially

## Sessions

1. **Agent A** -- Check if `setup/lock.json` has `"locked": false`. If so, acquire the lock by setting `"locked": true, "holder": "agent_a"`. Write `"AGENT_A_WAS_HERE"` to `setup/resource.txt`. Release the lock by setting `"locked": false`.
2. **Agent B** -- Same pattern: acquire lock, append `"AGENT_B_WAS_HERE"` to `setup/resource.txt`, release lock.
3. **Counter** -- Read `setup/resource.txt` and write the number of lines to `setup/answer.txt`.

## Constraints

- `setup/lock.json` is pre-created with `{"locked": false, "holder": null}`.
- `setup/answer.txt` must contain `"2"`.
- `setup/resource.txt` must contain both `AGENT_A_WAS_HERE` and `AGENT_B_WAS_HERE`.
- `setup/lock.json` must have `"locked": false` after all steps (lock released).
