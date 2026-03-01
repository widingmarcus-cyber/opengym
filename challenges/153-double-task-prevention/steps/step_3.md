# Step 3: Verify No Duplicates

You are acting as the **Verifier**.

Read `setup/task_registry.json` which contains task assignments for both Agent A and Agent B.

**Your task:**

1. Collect all task IDs assigned across both agents.
2. Count the total number of assigned tasks.
3. Check for any duplicates (task IDs that appear under more than one agent).
4. Write the result to `setup/answer.json` with keys `"total_assigned"` (total count of task IDs across all agents) and `"duplicates"` (count of task IDs that appear under more than one agent).
