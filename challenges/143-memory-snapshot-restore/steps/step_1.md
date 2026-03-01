# Step 1: Initialize State and Take First Snapshot

Create the initial application state and save your first snapshot.

1. Write the following initial state to `setup/state.json`:

```json
{"users": ["alice"], "config": {"theme": "light"}}
```

2. Copy the exact contents of `setup/state.json` to `setup/snapshots/snap_1.json` as a snapshot.

The state tracks a list of users and a configuration object. Snapshots are exact copies of the state at a point in time, allowing you to restore to a known-good state later.

Both `setup/state.json` and `setup/snapshots/` will persist to subsequent sessions.
