# Step 1: Initialize State and History

Create the initial account state and version history.

1. Write the following initial state to `setup/state.json`:

```json
{"balance": 100, "transactions": []}
```

2. Write the following version history to `setup/history.json`:

```json
[{"version": 1, "state": {"balance": 100, "transactions": []}}]
```

The state tracks an account balance and a list of transactions. The history log records snapshots of the state at each version, enabling rollback if a transaction fails.

Both files will persist to subsequent sessions.
