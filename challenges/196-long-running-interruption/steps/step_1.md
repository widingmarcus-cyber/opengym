# Step 1: Process Items with Interruption

You have a batch job that needs to process items 1 through 10 sequentially.

Process items 1, 2, 3, 4, 5, 6, 7 -- then an interruption occurs. You cannot process items 8, 9, 10 in this session.

Write your progress to `setup/progress.json`:

```json
{
  "completed": [1, 2, 3, 4, 5, 6, 7],
  "remaining": [8, 9, 10],
  "interrupted": true
}
```

This file will persist to the next session so the job can resume.
