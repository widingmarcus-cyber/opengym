# Step 2: Resume and Complete

Resume processing from your checkpoint. Read `setup/checkpoint.json` to determine which records have already been processed. Complete any remaining records that were not finished in Step 1.

Write the full results (both previously checkpointed and newly processed records) to `setup/output.json`. Do not reprocess records that are already in the checkpoint.

Ensure the final `setup/output.json` contains all 20 transformed records.
