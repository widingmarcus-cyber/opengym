# Step 1: Start the Pipeline

## Task

You have a 5-stage data pipeline defined in `setup/pipeline_config.json`. Each stage transforms the data from `setup/raw_data.json`.

1. Read `setup/raw_data.json` — it contains an array of numbers.
2. Execute stages 1-3 of the pipeline:
   - **Stage 1 (filter):** Remove all negative numbers
   - **Stage 2 (transform):** Square each remaining number
   - **Stage 3 (sort):** Sort the results in ascending order
3. Save your progress:
   - Write `setup/state.json` with: `{"completed_stages": [1, 2, 3], "intermediate_data": <result after stage 3>}`
   - Write `setup/checkpoint.json` with: `{"stage": 3, "timestamp": "<ISO timestamp>", "record_count": <number of records after stage 3>}`

Stages 4-5 will be completed in Session 2. The "crash" happens here — only state.json and checkpoint.json survive.
