# Step 2: Summarize Results

You are acting as the **Summarizer**.

Read `setup/results.json` from the previous step. It contains 5 subtask results, some succeeded and some failed.

**Your task:**

1. Count the number of subtasks with `"status": "success"`.
2. Count the number of subtasks with `"status": "failed"`.
3. Collect the IDs of all failed subtasks.
4. Write the summary to `setup/answer.json` with keys:
   - `"total_succeeded"`: count of successful subtasks
   - `"total_failed"`: count of failed subtasks
   - `"failed_ids"`: array of IDs of failed subtasks
