# Step 2: Break the Cycle

You are acting as the **Resolver**.

Read `setup/resolution.json` from the previous step. It describes the 3-node cycle and which node to break at.

**Your task:**

1. Break the cycle by providing a default output for the node specified in `break_at`. For example, if `break_at` is `"A"`, create `setup/node_A_output.txt` with content `default_A`.
2. Write `CYCLE_BROKEN` to `setup/answer.txt`.

After this step:
- The default output file for the broken node should exist
- `setup/answer.txt` should contain `CYCLE_BROKEN`
