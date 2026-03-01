# Challenge 207: Replay Determinism

## Difficulty: Medium
## Category: Failure Recovery

## Description

An operation log (`setup/operation_log.json`) records a series of transformations applied to a dataset. The original code (`setup/replayer.py`) is NON-deterministic — it uses random number generation and timestamps that produce different results each replay.

Your job:
1. Read `setup/operation_log.json` — each entry has an operation type, parameters, and a `seed` value for reproducibility.
2. Fix `setup/replayer.py` so that replaying the log is deterministic: given the same log, it always produces the same output.
3. The key fix: use the `seed` from each log entry to seed the RNG before each operation. Replace timestamp-dependent values with the `fixed_timestamp` from the log entry.
4. Run the fixed replayer to produce `setup/replay_output.json`.
5. Run it a second time to produce `setup/replay_output_2.json`.
6. Write `setup/determinism_proof.json` confirming the two outputs are identical.

## Expected Output

- `setup/replayer.py` — fixed to be deterministic
- `setup/replay_output.json` — first replay result
- `setup/replay_output_2.json` — second replay result (must be identical to first)
- `setup/determinism_proof.json` — JSON with keys: `outputs_match` (true), `operations_replayed` (int), `seeds_used` (list of seed values)

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
