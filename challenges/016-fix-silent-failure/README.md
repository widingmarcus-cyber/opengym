# Challenge 016: Fix the Silent Failures

## Difficulty: Medium

## Task

The file `setup/pipeline.py` implements a data-processing pipeline with three stages: validate, transform, and aggregate. The pipeline is supposed to process a list of records (dicts) through each stage.

However, each stage has a bare `except` clause that silently swallows all exceptions, causing the pipeline to return wrong or empty results without any error.

**Your job:** Fix the error handling so that real bugs are raised (not silently swallowed) while still handling expected edge cases gracefully.

## Functions

1. `validate(records)` -- Filters records, keeping only those with required keys ('name', 'amount'). Should raise TypeError if records is not a list.
2. `transform(records)` -- Transforms each record: uppercases 'name', converts 'amount' to float, adds 'processed' flag. Should raise ValueError if amount cannot be converted.
3. `aggregate(records)` -- Returns a summary dict with 'total_amount', 'count', and 'names' list. Should raise TypeError if records is not a list.
4. `process_records(records)` -- Runs the full pipeline: validate -> transform -> aggregate. Should propagate exceptions from the stages.

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- Errors from invalid data types should propagate (not be silently caught)
- Missing keys in individual records should be handled gracefully (skip the record)
