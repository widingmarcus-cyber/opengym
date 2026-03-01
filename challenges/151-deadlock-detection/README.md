# Challenge 151: Deadlock Detection (2-node)

**Difficulty:** Hard
**Category:** agent-collaboration
**Dimension:** multi-agent
**Type:** Multi-session (2 steps)

## Objective

Detect a circular dependency between two agents that creates a deadlock, and resolve it by breaking the cycle.

## What This Tests

- Detecting circular dependencies in a dependency graph
- Understanding deadlock conditions (mutual waiting)
- Breaking deadlock cycles by providing default values
- Writing a resolution plan

## Sessions

1. **Detector** -- Read `setup/dependencies.json` which describes a circular dependency: Agent A waits for Agent B's output, and Agent B waits for Agent A's output. Detect the cycle and write a resolution plan to `setup/resolution.json`.
2. **Resolver** -- Implement the resolution: write a default value (`"default_a"`) to `setup/agent_a_output.txt` to break the cycle. Write `"DEADLOCK_RESOLVED"` to `setup/answer.txt`.

## Constraints

- `setup/dependencies.json` is pre-created with the circular dependency.
- `setup/resolution.json` must exist and describe the cycle.
- `setup/agent_a_output.txt` must exist (breaking the cycle).
- `setup/answer.txt` must contain `"DEADLOCK_RESOLVED"`.
