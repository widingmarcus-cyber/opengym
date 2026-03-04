# Step 1: Initialize the Key-Value Store

Create a key-value store in `setup/store.json`. Add the following 10 entries exactly as specified.

Each entry is a JSON object with fields: `key`, `value`, `tag`, `version`, and `timestamp`. The store is a JSON object where keys map to entry objects.

## Entries to Add

| key | value | tag | version | timestamp |
|-----|-------|-----|---------|-----------|
| `app_config` | `{"timeout": 30, "retries": 3}` | `config` | 1 | `2025-11-01T09:00:00Z` |
| `app_secret` | `"s3cr3t-k3y-2024"` | `config` | 1 | `2025-11-01T09:01:00Z` |
| `db_host` | `"postgres.internal:5432"` | `system` | 1 | `2025-11-01T09:02:00Z` |
| `db_pool_size` | `10` | `system` | 1 | `2025-11-01T09:03:00Z` |
| `cache_ttl` | `3600` | `config` | 1 | `2025-11-01T09:04:00Z` |
| `temp_upload_01` | `"/tmp/upload_abc.dat"` | `temp` | 1 | `2025-11-01T09:05:00Z` |
| `temp_session_x` | `{"user": "alice", "exp": 9999}` | `temp` | 1 | `2025-11-01T09:06:00Z` |
| `user_prefs` | `{"theme": "dark", "lang": "en"}` | `data` | 1 | `2025-11-01T09:07:00Z` |
| `analytics_queue` | `[1, 2, 3, 4, 5]` | `data` | 1 | `2025-11-01T09:08:00Z` |
| `app_feature_flags` | `{"beta": true, "v2": false}` | `config` | 1 | `2025-11-01T09:09:00Z` |

## Output

Write the store to `setup/store.json` as a JSON object mapping each key to its entry object. Example structure:

```json
{
  "app_config": {
    "key": "app_config",
    "value": {"timeout": 30, "retries": 3},
    "tag": "config",
    "version": 1,
    "timestamp": "2025-11-01T09:00:00Z"
  },
  ...
}
```

Ensure the file is valid JSON and contains exactly 10 entries.
