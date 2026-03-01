# Step 2: Resolve the Deadlock

You are acting as the **Resolver**.

Read `setup/resolution.json` from the previous step. It describes a deadlock between Agent A and Agent B.

**Your task:** Implement the resolution:

1. Write a default value `default_a` to `setup/agent_a_output.txt`. This breaks the cycle because Agent B was waiting for this file.
2. Write `DEADLOCK_RESOLVED` to `setup/answer.txt`.

After this step:
- `setup/agent_a_output.txt` should contain `default_a`
- `setup/answer.txt` should contain `DEADLOCK_RESOLVED`
