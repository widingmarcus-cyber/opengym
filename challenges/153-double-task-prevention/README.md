# Challenge 153: Double Task Assignment Prevention

**Difficulty:** Medium
**Category:** task-splitting
**Dimension:** multi-agent
**Type:** Multi-session (3 steps)

## Objective

Ensure that when multiple agents claim tasks from a shared task list, no task is assigned to more than one agent.

## What This Tests

- Reading a shared task registry to avoid double-assignment
- Claiming only unclaimed tasks
- Verifying no duplicates across agents
- Coordinating task distribution among multiple agents

## Sessions

1. **Agent A Claims** -- Read `setup/tasks.json` (5 tasks). Claim tasks 1, 2, 3 by writing them to `setup/task_registry.json` under `"agent_a"`.
2. **Agent B Claims** -- Read `setup/task_registry.json` to see which tasks are already claimed. Claim the remaining tasks (4, 5) under `"agent_b"`. Must NOT claim any already-claimed task.
3. **Verifier** -- Verify all 5 tasks are assigned with no duplicates. Write `setup/answer.json` with `{"total_assigned": 5, "duplicates": 0}`.

## Constraints

- `setup/tasks.json` is pre-created with 5 tasks.
- `setup/task_registry.json` is pre-created as empty `{}`.
- No task ID may appear under more than one agent.
- `setup/answer.json` must have `total_assigned=5` and `duplicates=0`.
