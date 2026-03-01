# Challenge 211: Multi-Step Rollback

## Difficulty: Hard
## Category: Failure Recovery

## Description

A deployment pipeline executed 6 steps, but step 5 failed. Steps 1-4 completed successfully and modified system state. You must roll back steps 1-4 in reverse order to restore the original state.

Files:
- `setup/current_state.json` — the system state after steps 1-4 executed (step 5 failed, step 6 never ran)
- `setup/deployment_log.json` — log of all 6 steps with their operations and rollback instructions
- `setup/rollback_procedures.json` — describes the rollback operation types

Your job:
1. Read the deployment log to understand what steps 1-4 did and what their rollback operations are.
2. Start from `current_state.json` and apply the rollback operations in REVERSE order (step 4 first, then 3, 2, 1).
3. Write the computed rolled-back state to `setup/rolled_back_state.json`.
4. Write `setup/rollback_log.json` documenting each rollback action taken.

## Expected Output

- `setup/rolled_back_state.json` — the state after all rollback operations have been applied
- `setup/rollback_log.json` — JSON with keys: `steps_rolled_back` (list of step numbers in rollback order), `all_reverted` (boolean), `final_matches_original` (boolean)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
