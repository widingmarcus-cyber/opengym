# Challenge 134: Indexed Retrieval Constraint

**Difficulty:** Hard
**Category:** memory-state
**Dimension:** memory
**Type:** Multi-session (2 steps)

## Objective

Demonstrate that your agent can build a lightweight index over a set of data files, and then use that index to efficiently retrieve and aggregate information without loading all files.

## What This Tests

- Building an index structure that maps categories to filenames
- Using the index to selectively read only relevant files
- Correct aggregation of values from selected records

## Sessions

1. **Build Index** -- Read all 20 JSON record files in `setup/data/` and build an index in `setup/index.json` that maps each category to a list of filenames containing records of that category. Do NOT copy file contents into the index -- only filenames.
2. **Query by Index** -- Using `setup/index.json`, identify which files belong to category "B". Read only those files, sum their values, and write the result to `setup/answer.txt`.

## Constraints

- `setup/index.json` must be a JSON object mapping category strings to arrays of filenames.
- `setup/answer.txt` must contain the correct sum of all values in category B.
- The 20 record files in `setup/data/` must not be modified.
