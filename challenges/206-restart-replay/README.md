# Challenge 206: Restart Replay

## Difficulty: Hard
## Category: Failure Recovery
## Type: Multi-Session

## Description

This is a two-session challenge implementing Write-Ahead Logging (WAL) for crash recovery.

### Session 1 (step_1.md)
Build a WAL-based system: perform operations on a bank account ledger, logging each operation to a WAL BEFORE applying it. Save the WAL for crash recovery.

### Session 2 (step_2.md)
After a simulated crash, replay the WAL to reconstruct the ledger state from scratch.

See `steps/step_1.md` and `steps/step_2.md` for detailed instructions.

## Persistence

Between sessions, only these files survive:
- `setup/wal.json`
- `setup/state.json`

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
