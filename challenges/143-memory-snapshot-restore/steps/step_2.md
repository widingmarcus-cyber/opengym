# Step 2: Modify State, Snapshot, and Restore

Read `setup/state.json` and make the following modifications:

## Modify State
1. Add `"bob"` to the `users` array (so it becomes `["alice", "bob"]`).
2. Change `config.theme` from `"light"` to `"dark"`.
3. Write the updated state to `setup/state.json`.

## Take Snapshot
4. Copy the current `setup/state.json` to `setup/snapshots/snap_2.json`.

## Something Went Wrong -- Restore!
5. **Important:** Something went wrong with the changes above. You need to restore the state to how it was before these modifications. Copy the contents of `setup/snapshots/snap_1.json` back into `setup/state.json`, overwriting the current state.

After this step:
- `setup/state.json` should match `snap_1.json`: `{"users": ["alice"], "config": {"theme": "light"}}`
- `setup/snapshots/snap_1.json` should still exist (the original snapshot)
- `setup/snapshots/snap_2.json` should also exist (the snapshot of the modified state)
