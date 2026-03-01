# Challenge 132: Partial Write Interruption

**Difficulty:** Hard
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (2 steps)

## Objective

A pre-existing data file contains 5 records, but one record has been corrupted (simulating a partial write interruption). The agent must detect the corruption, fix it, and then add 5 new records. In the second session, the agent reads the file and reports the total number of valid records.

## What This Tests

- Detection of data corruption in a structured JSON file
- Ability to repair corrupted data while preserving valid records
- Correct addition of new records to an existing dataset
- Data integrity validation across sessions

## Sessions

1. **Fix and Extend** -- Read data.json, detect that record 3 has a truncated "value" field, fix it to a reasonable complete value, and add 5 new records (IDs 6-10).
2. **Count Records** -- Read data.json and write the total count of valid records to answer.txt.

## Constraints

- After step 1, `setup/data.json` must contain exactly 10 records
- Record 3's "value" field must be repaired (not truncated)
- `setup/answer.txt` must contain exactly the string "10"
