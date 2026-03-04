# Step 3: Implement Module C

Implement `module_c` in `setup/module_c.py`.

## Requirements

Create a function `summarize_records(records)` that:
- Takes a list of record dicts (each with "name" and "priority" fields)
- Returns a dict with:
  - `"count"`: number of records (int)
  - `"avg_priority"`: average of all priority values, rounded to 2 decimal places (float)
  - `"names"`: sorted list of all name values (alphabetically ascending)

## Versioning

Save a versioned copy of your implementation as `setup/module_c_v3.py`.
