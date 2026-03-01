# Step 2: Resume and Complete

Read `setup/progress.json` to determine where the batch job was interrupted.

Resume processing from the first remaining item and complete all remaining items.

Update `setup/progress.json` to reflect full completion:
- Move all remaining items to the `completed` list
- Set `remaining` to an empty array
- Set `interrupted` to `false`

Write `setup/answer.json` with:
- `"total_completed"`: total number of items processed across both sessions
- `"resumed_from"`: the first item ID that was resumed in this session
