# Step 2: Verify Recovery

You are acting as the **Verifier**.

1. Read `setup/result.txt`. It should contain `RECOVERED`.
2. Read `setup/lock.json`. It should have `"locked": false` (lock was released).
3. If both conditions are met, write `LOCK_RECOVERED` to `setup/answer.txt`.

Write just the text to `setup/answer.txt`:
```
LOCK_RECOVERED
```
