# Step 1: Store Cache Entries

Read `setup/cache.json`. It contains 5 cache entries, each with the following fields:

- `key` — a unique identifier for the entry
- `value` — the cached data
- `ttl_seconds` — how long the entry is valid (in seconds)
- `created_at` — the ISO 8601 timestamp when the entry was created

All entries were created at `2024-01-01T00:00:00Z`. Three entries have `ttl_seconds: 60` (expire after 1 minute) and two entries have `ttl_seconds: 3600` (expire after 1 hour).

The current time is `2024-01-01T00:05:00Z` (5 minutes after creation).

Review the entries and ensure you understand which ones will be expired by the 5-minute mark. The file `setup/cache.json` will persist to the next session.
