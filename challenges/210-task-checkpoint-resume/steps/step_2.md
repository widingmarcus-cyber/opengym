# Step 2: Resume from Checkpoint

## Task

The process crashed at batch 12. Only checkpoints and progress.json survived.

1. Read `setup/progress.json` to find the last valid checkpoint.
2. Load `setup/checkpoints/checkpoint_10.json` to get results for batches 1-10.
3. Resume processing from batch 11 through batch 20:
   - For each batch, read from `setup/batches.json` and compute the sum
4. Write the complete results to `setup/final_results.json`:
   ```json
   {
     "results": [{"batch_id": 1, "sum": ..., "status": "completed"}, ...],
     "resumed_from_checkpoint": 10,
     "total_batches": 20,
     "all_complete": true
   }
   ```
5. Write a final checkpoint: `setup/checkpoints/checkpoint_20.json` with all 20 results.
