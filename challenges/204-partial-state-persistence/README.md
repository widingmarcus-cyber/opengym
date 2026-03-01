# Challenge 204: Partial State Persistence

## Difficulty: Hard
## Category: Failure Recovery
## Type: Multi-Session

## Description

This is a two-session challenge simulating a crash between processing stages.

### Session 1 (step_1.md)
You start a multi-stage data pipeline. Complete stages 1-3 and save state/checkpoints before the "crash."

### Session 2 (step_2.md)
After the crash, detect what was persisted, identify what was lost, and reconstruct the complete result.

See `steps/step_1.md` and `steps/step_2.md` for detailed instructions.

## Persistence

Between sessions, only these files survive:
- `setup/state.json`
- `setup/checkpoint.json`

All other runtime data is lost.

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
