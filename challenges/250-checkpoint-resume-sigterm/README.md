# Challenge 250: Checkpoint-Resume Under SIGTERM

## Objective

Process 20 records from `setup/records.json`, applying transformation rules from `setup/rules.json`. Write the fully transformed results to `setup/output.json`.

You should checkpoint your progress to `setup/checkpoint.json` periodically so that you can resume from where you left off if your process is interrupted.

## Transformation Rules

For each record, apply the category-based multiplier from `setup/rules.json`:

- Multiply the record's `value` by the multiplier for its `category`
- Round the result to the number of decimal places specified in `round_to`
- Add a `processed_at` field with a timestamp string to each output record

## Output Format

`setup/output.json` should be a JSON array of objects, each with:

- `id` — from the input record
- `name` — from the input record
- `value` — the transformed value (original value * category multiplier, rounded)
- `category` — from the input record
- `processed_at` — a timestamp string indicating when the record was processed

## Checkpointing

Save your progress to `setup/checkpoint.json` after processing each record. This file should contain enough information to resume processing without re-doing completed work. If interrupted and restarted, read the checkpoint to determine which records still need processing.

## Constraints

- All 20 records must appear exactly once in the final output
- Do not reprocess records that were already checkpointed
- Only modify `setup/output.json` and `setup/checkpoint.json`
