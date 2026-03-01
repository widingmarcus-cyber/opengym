# Challenge 210: Task Checkpoint Resume

## Difficulty: Hard
## Category: Failure Recovery
## Type: Multi-Session

## Description

This is a two-session challenge. A long-running computation processes 20 data batches. Checkpoints are written every 5 batches. After a crash, resume from the last valid checkpoint.

### Session 1 (step_1.md)
Process batches 1-12, writing checkpoints at batch 5 and 10. The "crash" happens at batch 12 (mid-batch).

### Session 2 (step_2.md)
Resume from the last valid checkpoint (batch 10) and complete all 20 batches.

See `steps/step_1.md` and `steps/step_2.md` for detailed instructions.

## Persistence

Between sessions, these survive:
- `setup/checkpoints/` directory
- `setup/progress.json`

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
