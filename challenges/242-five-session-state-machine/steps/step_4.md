# Step 4: Query the Store

Read `setup/store.json` and answer the following queries. Write all answers to `setup/answers.json`.

## Queries

1. **count_by_tag**: An object mapping each tag to the number of entries with that tag. Example: `{"config": 3, "data": 2, "system": 1}`

2. **highest_version**: The maximum `version` value across all entries in the store (an integer).

3. **total_entries**: The total number of entries in the store (an integer).

4. **keys_matching_prefix**: A sorted list of all keys that start with the prefix `"app_"`. Example: `["app_config", "app_secret"]`

## Output

Write `setup/answers.json` in exactly this format:

```json
{
  "count_by_tag": { ... },
  "highest_version": ...,
  "total_entries": ...,
  "keys_matching_prefix": [ ... ]
}
```

Do not modify `setup/store.json` in this step.
