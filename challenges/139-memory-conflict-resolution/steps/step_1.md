# Step 1: Initialize Shared State and Policy

Create the initial shared configuration state. Write the following JSON to `setup/state.json`:

```json
{"config": {"port": 3000, "host": "localhost"}}
```

Then write the conflict resolution policy to `setup/policy.txt`. The policy is:

```
last-write-wins
```

This policy means that when multiple agents write to the same field, the most recent write takes precedence without requiring any merge logic.

Both files will persist to subsequent sessions.
