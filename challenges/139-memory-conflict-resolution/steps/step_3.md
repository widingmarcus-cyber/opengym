# Step 3: Agent B Writes with Conflict Resolution

You are Agent B. Your task is to update the server port configuration, but you must first check the conflict resolution policy.

1. Read `setup/policy.txt` to determine the conflict resolution policy.
2. The policy is `last-write-wins`, which means your write should succeed and overwrite any previous value.
3. Read `setup/state.json` and update the `port` field under `config` to `9090`. Write the updated state back to `setup/state.json`.
4. Write the final port value to `setup/answer.txt` (just the number, e.g., `9090`).

Keep all other fields (like `host`) unchanged.
