# Challenge 211: Multi-Step Rollback

## Difficulty: Hard
## Category: Failure Recovery

## Description

A deployment pipeline executed 6 steps, but step 5 failed. Steps 1-4 completed successfully and modified system state. You must roll back steps 1-4 in reverse order to restore the original state.

Files:
- `setup/original_state.json` — the system state before the deployment started
- `setup/current_state.json` — the system state after steps 1-4 executed (step 5 failed, step 6 never ran)
- `setup/deployment_log.json` — log of all 6 steps with their operations and rollback instructions
- `setup/rollback_procedures.json` — detailed rollback procedure for each step type

Your job:
1. Read the deployment log to understand what steps 1-4 did.
2. Execute the rollback in REVERSE order (step 4 first, then 3, 2, 1).
3. Write the rolled-back state to `setup/rolled_back_state.json` — it must match `original_state.json`.
4. Write `setup/rollback_log.json` documenting each rollback action taken.

## Expected Output

- `setup/rolled_back_state.json` — must match original_state.json exactly
- `setup/rollback_log.json` — JSON with keys: `steps_rolled_back` (list of step numbers in rollback order: [4,3,2,1]), `all_reverted` (true), `final_matches_original` (true)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
