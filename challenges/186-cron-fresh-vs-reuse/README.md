# Challenge 186: Cron Fresh vs Reuse

**Difficulty:** medium
**Category:** task-sequencing
**Dimension:** planning
**Type:** multi-session (2 steps)

## Description

You are managing a task scheduler that supports two execution policies: **fresh** and **reuse**.

- **fresh**: The task must be executed with a clean, new context every time it runs. No state from previous runs carries over.
- **reuse**: The task reuses existing context from a previous run if available.

Your job is to execute a schedule across two sessions, properly enforcing the policy for each task, and produce a summary of executions.

## Objectives

### Step 1
- Read `setup/schedule.json` which defines tasks with execution policies.
- Execute all tasks and record the results in `setup/execution_log.json`.
- For "fresh" policy tasks, record that they received a clean context.
- For "reuse" policy tasks, record that they use existing context.

### Step 2
- The schedule runs again. Execute all tasks again following the same policy rules.
- "fresh" tasks are re-executed from scratch (clean context).
- "reuse" tasks note they are reusing context from the previous run.
- Update `setup/execution_log.json` with all executions from both runs.
- Write `setup/answer.json` with the count of fresh vs reuse executions across both runs.

## Expected Output

`setup/answer.json`:
```json
{"fresh_count": 4, "reuse_count": 2}
```

(t1 and t3 are fresh in both runs = 4, t2 is reuse in both runs = 2)
