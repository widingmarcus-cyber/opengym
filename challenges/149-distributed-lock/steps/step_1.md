# Step 1: Agent A Acquires Lock and Writes

You are acting as **Agent A**.

Follow this lock protocol to safely write to the shared resource:

1. Read `setup/lock.json`. Check that `"locked"` is `false`.
2. **Acquire the lock:** Update `setup/lock.json` to:
   ```json
   {"locked": true, "holder": "agent_a"}
   ```
3. **Write to the resource:** Write `AGENT_A_WAS_HERE` as the first line of `setup/resource.txt`.
4. **Release the lock:** Update `setup/lock.json` to:
   ```json
   {"locked": false, "holder": null}
   ```

You MUST release the lock after writing to the resource.
