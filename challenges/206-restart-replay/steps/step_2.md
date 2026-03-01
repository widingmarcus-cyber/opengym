# Step 2: Replay WAL to Reconstruct State

## Task

The process crashed. Only `setup/wal.json` and `setup/state.json` survived.
The `setup/initial_ledger.json` is still available (it's read-only source data).

1. Read `setup/initial_ledger.json` to get the starting state.
2. Read `setup/wal.json` to get the operation log.
3. Replay all WAL entries against the initial ledger to reconstruct the final state.
4. Verify that the replayed state matches `setup/state.json`.
5. Write `setup/replay_result.json` with:
   ```json
   {
     "replay_successful": true,
     "operations_replayed": <number>,
     "final_ledger": {<account_id: balance>},
     "matches_saved_state": true
   }
   ```
