# Step 1: Recover Stale Lock

You are acting as the **Recovery Agent**.

Read `setup/lock.json`. It currently contains:

```json
{"locked": true, "holder": "stale_process", "acquired_at": "2024-01-01T00:00:00Z"}
```

The lock timeout is 60 seconds. This lock has been held since January 1, 2024 -- far exceeding the timeout.

**Your task:**

1. Detect that the lock is stale (held for over 24 hours, well past the 60-second timeout).
2. **Force-release the lock:** Set `"locked": false` in `setup/lock.json`.
3. **Acquire the lock yourself:** Set `"locked": true, "holder": "recovery_agent"` in `setup/lock.json`.
4. **Write to the resource:** Write `RECOVERED` to `setup/result.txt`.
5. **Release the lock:** Set `"locked": false, "holder": null` in `setup/lock.json`.

After this step:
- `setup/result.txt` should contain `RECOVERED`
- `setup/lock.json` should have `"locked": false`
