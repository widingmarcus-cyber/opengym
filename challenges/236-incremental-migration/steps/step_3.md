# Step 3: Verify and Reconcile

## Task

Verify all 20 records have been migrated correctly and produce a reconciliation report.

1. Read `setup/batch_1.json` and `setup/batch_2.json`.
2. Read `setup/legacy_data.json` (source of truth for record count).
3. Verify every legacy record has a corresponding migrated record.
4. Write `setup/reconciliation.json`.

## Expected Output

`setup/reconciliation.json`:
```json
{
  "total_source_records": 20,
  "total_migrated_records": 20,
  "missing_records": [],
  "schema_version": "v2",
  "all_records_migrated": true,
  "field_coverage": {
    "<field_name>": <count of records with this field>,
    ...
  },
  "status": "complete"
}
```

## Notes

- `missing_records` should list IDs of any records in the legacy data not found in batches.
- `field_coverage` should show how many records have each field from the v2 schema.
- `status` is "complete" only if all records are migrated with correct schema.
