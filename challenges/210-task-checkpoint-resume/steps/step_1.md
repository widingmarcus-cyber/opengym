# Step 1: Process Batches and Write Checkpoints

## Task

You have 20 data batches in `setup/batches.json`. Each batch is an array of numbers. Processing a batch means computing its sum.

1. Read `setup/batches.json`.
2. Process batches 1 through 12:
   - For each batch, compute the sum of its numbers
   - Store as `{"batch_id": N, "sum": <sum>, "status": "completed"}`
3. Write checkpoints:
   - After batch 5: write `setup/checkpoints/checkpoint_5.json` containing results for batches 1-5
   - After batch 10: write `setup/checkpoints/checkpoint_10.json` containing results for batches 1-10
   - Batch 12 "crashes" — checkpoint at 10 is the last valid one
4. Write `setup/progress.json` with:
   ```json
   {
     "last_valid_checkpoint": 10,
     "batches_completed": 10,
     "batches_lost": [11, 12],
     "total_batches": 20
   }
   ```

Note: Do NOT write results for batches 11-12 to any checkpoint. They represent lost work.
