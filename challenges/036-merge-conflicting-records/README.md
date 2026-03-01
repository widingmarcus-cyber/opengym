# Challenge 036: Merge Conflicting Records

## Difficulty: Hard

## Task

Reconcile two datasets that contain overlapping records with conflicting values. Implement the merge logic in `setup/merger.py`.

## Requirements

Implement this function in `setup/merger.py`:

1. `merge(records_a, records_b, key="id")` -- Merge two lists of dictionaries based on a shared key field. Return a dictionary with two keys:
   - `"merged"`: A list of merged records. For records that exist in only one dataset, include them as-is. For records that share the same key value in both datasets, keep the version with the more recent `"updated_at"` timestamp.
   - `"conflicts"`: A list of dictionaries describing each conflict found. Each conflict entry should have: `{"key": <key_value>, "field": <field_name>, "value_a": <value_from_a>, "value_b": <value_from_b>}`. Report one conflict entry per differing field (exclude `"updated_at"` from conflict reporting).

## Data Format

Records in both `setup/dataset_a.json` and `setup/dataset_b.json` are dictionaries with:
- `id`: Unique identifier (string)
- `name`: A person's name
- `email`: Email address
- `department`: Department name
- `updated_at`: ISO 8601 timestamp indicating when the record was last modified

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules
- The merged list should be sorted by the key field
- Conflicts should be reported for all fields that differ (except `updated_at`)
- The `key` parameter allows merging on any field, not just `"id"`
