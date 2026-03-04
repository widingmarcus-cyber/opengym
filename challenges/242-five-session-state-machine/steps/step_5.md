# Step 5: Integrity Manifest

Read `setup/store.json` and compute an integrity manifest.

## Checksum Computation

1. Serialize the store to a JSON string using `json.dumps(store, sort_keys=True)` with **no indentation** (no `indent` parameter).
2. Encode the string as UTF-8.
3. Compute the SHA256 hash of the encoded bytes.
4. The checksum is the hex digest (lowercase).

## Manifest

Write `setup/manifest.json` with the following fields:

```json
{
  "checksum": "<sha256 hex digest>",
  "entry_count": <number of entries>,
  "tags": ["<sorted unique list of tags>"],
  "last_modified": "<current ISO 8601 timestamp>"
}
```

- `checksum`: The SHA256 hex digest computed above.
- `entry_count`: The total number of entries in the store.
- `tags`: A sorted list of unique tag values across all entries.
- `last_modified`: A valid ISO 8601 timestamp string representing the current time when you write the manifest.

## Output

Write `setup/manifest.json`. Do not modify `setup/store.json` in this step.
