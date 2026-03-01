# Challenge 152: Deadlock Detection (3-node)

**Difficulty:** Hard
**Category:** agent-collaboration
**Dimension:** multi-agent
**Type:** Multi-session (2 steps)

## Objective

Detect a circular dependency among three nodes (A, B, C) that creates a deadlock cycle, and resolve it by breaking the cycle at one point.

## What This Tests

- Detecting cycles in a 3-node dependency graph
- Tracing dependency chains: A waits for B, B waits for C, C waits for A
- Breaking multi-node deadlock cycles
- Writing structured resolution plans

## Sessions

1. **Detector** -- Read `setup/graph.json` which describes a 3-node cycle: A waits for B, B waits for C, C waits for A. Detect the cycle and write it to `setup/resolution.json` as `{"cycle": ["A", "B", "C", "A"], "break_at": "..."}`.
2. **Resolver** -- Break the cycle by providing a default output for one node. Write `"CYCLE_BROKEN"` to `setup/answer.txt`.

## Constraints

- `setup/graph.json` is pre-created with the 3-node dependency graph.
- `setup/resolution.json` must contain the correct cycle and a `break_at` field.
- `setup/answer.txt` must contain `"CYCLE_BROKEN"`.
