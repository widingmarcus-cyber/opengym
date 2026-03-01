# Step 2: Agent B Acquires Lock and Writes

You are acting as **Agent B**.

Follow the same lock protocol to safely write to the shared resource:

1. Read `setup/lock.json`. Check that `"locked"` is `false`.
2. **Acquire the lock:** Update `setup/lock.json` to:
   ```json
   {"locked": true, "holder": "agent_b"}
   ```
3. **Append to the resource:** Append `AGENT_B_WAS_HERE` as a new line to `setup/resource.txt`. Do NOT overwrite Agent A's line.
4. **Release the lock:** Update `setup/lock.json` to:
   ```json
   {"locked": false, "holder": null}
   ```

After this step, `setup/resource.txt` should have two lines:
```
AGENT_A_WAS_HERE
AGENT_B_WAS_HERE
```

You MUST release the lock after writing to the resource.
