# Step 2: Schema Change and Second Batch

## Task

A schema change has been introduced. Migrate the second batch AND update the first batch.

1. Read `setup/schema_v2_changes.json` for the schema updates.
2. Migrate records 11-20 from `setup/legacy_data.json` using the updated schema (v2). Write to `setup/batch_2.json`.
3. Retroactively update `setup/batch_1.json` to conform to schema v2 as well.

## Schema V2 Changes

The schema v2 changes file specifies:
- `new_fields`: fields to add with default values
- `renamed_fields`: fields that have been renamed again
- `removed_fields`: fields to drop

## Expected Output

`setup/batch_2.json`:
```json
{
  "batch_number": 2,
  "record_count": 10,
  "schema_version": "v2",
  "records": [ ... ]
}
```

Updated `setup/batch_1.json` must also have `schema_version` set to "v2" and records updated accordingly.
