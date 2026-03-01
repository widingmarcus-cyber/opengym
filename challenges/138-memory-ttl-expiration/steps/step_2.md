# Step 2: Remove Expired Entries

The current time is `2024-01-01T00:05:00Z` (300 seconds after the entries were created at `2024-01-01T00:00:00Z`).

An entry is expired if the elapsed time since `created_at` exceeds its `ttl_seconds`. That is:
- Elapsed = 300 seconds
- Entries with `ttl_seconds: 60` are expired (300 > 60)
- Entries with `ttl_seconds: 3600` are still valid (300 < 3600)

Read `setup/cache.json`, filter out all expired entries, and write the remaining valid entries to `setup/active_cache.json`.

The output file should be a JSON array containing only the non-expired entries, preserving their original structure.
