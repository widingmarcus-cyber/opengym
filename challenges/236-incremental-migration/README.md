# Challenge 236: Incremental Migration

## Objective

Perform an incremental data migration across 3 sessions. You must migrate records from a legacy schema to a new schema in batches, handle schema changes introduced mid-migration, and produce a final reconciliation report.

This is a **multi-session challenge** with 3 steps. See the `steps/` directory for per-step instructions.

## Setup

- `setup/legacy_data.json` - Source data in the legacy schema (20 records total).
- `setup/new_schema.json` - The target schema definition for the new system.
- `setup/schema_v2_changes.json` - Schema changes introduced in Step 2 (not available until Step 2).

## Overall Flow

1. **Step 1**: Migrate the first batch (records 1-10) to the new schema. Write `setup/batch_1.json`.
2. **Step 2**: Schema changes are introduced. Migrate second batch (records 11-20) using the updated schema, and retroactively update batch 1. Write `setup/batch_2.json` and update `setup/batch_1.json`.
3. **Step 3**: Verify all records are migrated, reconcile source vs. target, write `setup/reconciliation.json`.

## Constraints

- Records must be transformed according to the schema mappings.
- No records may be lost during migration.
- Schema changes in Step 2 must be applied to ALL records (including previously migrated ones).
