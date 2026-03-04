# Step 4: Create Pipeline

Create `setup/pipeline.py` that integrates all three modules.

## Requirements

1. Import `sort_records` from `setup/module_a.py`
2. Import `filter_records` from `setup/module_b.py`
3. Import `summarize_records` from `setup/module_c.py`

4. Implement `run_pipeline(records, min_priority)` that:
   - Filters records using `filter_records(records, min_priority)`
   - Sorts the filtered records using `sort_records(filtered)`
   - Summarizes the sorted records using `summarize_records(sorted)`
   - Returns the summary dict

5. Load the test data from `setup/test_data.json`
6. Run the pipeline with `min_priority=3`
7. Write the result to `setup/pipeline_result.json`

The pipeline should execute when the file is run directly (`if __name__ == "__main__"`).
