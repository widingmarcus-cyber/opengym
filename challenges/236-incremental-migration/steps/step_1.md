# Step 1: Migrate First Batch

## Task

Migrate records 1-10 from `setup/legacy_data.json` to the new schema defined in `setup/new_schema.json`.

1. Read the legacy data and new schema definition.
2. Transform records 1 through 10 according to the field mappings in `new_schema.json`.
3. Write the migrated records to `setup/batch_1.json`.

## Expected Output

`setup/batch_1.json`:
```json
{
  "batch_number": 1,
  "record_count": 10,
  "schema_version": "v1",
  "records": [
    { ... migrated record ... },
    ...
  ]
}
```

## Field Mappings (from new_schema.json)

Apply the `field_mappings` to transform legacy field names to new field names. Apply `type_conversions` to convert data types. Set `migration_status` to "migrated" on each record.
