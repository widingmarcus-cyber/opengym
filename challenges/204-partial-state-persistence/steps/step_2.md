# Step 2: Recover and Complete

## Task

The process crashed after stage 3. Only `setup/state.json` and `setup/checkpoint.json` survived.

1. Read `setup/state.json` and `setup/checkpoint.json` to determine what was completed.
2. Verify the checkpoint is valid (stage 3 completed, data is present).
3. Resume from stage 3's output and complete:
   - **Stage 4 (aggregate):** Compute `sum`, `count`, `mean` (rounded to 2 decimal places), `min`, `max` of the sorted data
   - **Stage 5 (report):** Produce the final report
4. Write `setup/final_report.json` with:
   ```json
   {
     "pipeline_complete": true,
     "stages_from_checkpoint": [4, 5],
     "stages_from_scratch": [1, 2, 3],
     "aggregation": {"sum": ..., "count": ..., "mean": ..., "min": ..., "max": ...},
     "recovered_from_crash": true
   }
   ```
