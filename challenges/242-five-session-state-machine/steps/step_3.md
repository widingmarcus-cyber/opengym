# Step 3: Compact the Store

Read `setup/store.json`. Remove all entries where **both** of the following conditions are true:

1. The entry's `tag` is `"temp"`
2. The entry's `version` is less than 3

## Compaction Report

Write a compaction report to `setup/compaction_report.json` listing the keys that were removed. The report format:

```json
{
  "removed_keys": ["key1", "key2", ...]
}
```

The `removed_keys` array should be sorted alphabetically.

## Output

Write the updated store (with temp entries removed) back to `setup/store.json`. Do not modify any non-temp entries. Do not modify entries that do not meet both removal conditions.
