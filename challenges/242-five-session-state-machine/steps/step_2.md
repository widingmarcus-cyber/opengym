# Step 2: Expand and Upgrade the Store

Read `setup/store.json`. Add the following 8 new entries. Then upgrade ALL entries in the store (both old and new) to version 2.

## New Entries to Add

| key | value | tag | version | timestamp |
|-----|-------|-----|---------|-----------|
| `temp_draft_99` | `"draft content here"` | `temp` | 1 | `2025-11-02T10:00:00Z` |
| `app_rate_limit` | `1000` | `config` | 1 | `2025-11-02T10:01:00Z` |
| `worker_count` | `4` | `system` | 1 | `2025-11-02T10:02:00Z` |
| `temp_lock_file` | `"/var/lock/process.pid"` | `temp` | 1 | `2025-11-02T10:03:00Z` |
| `user_history` | `["login", "view", "edit"]` | `data` | 1 | `2025-11-02T10:04:00Z` |
| `metrics_buffer` | `{"cpu": 45.2, "mem": 72.1}` | `data` | 1 | `2025-11-02T10:05:00Z` |
| `app_locale` | `"en-US"` | `config` | 1 | `2025-11-02T10:06:00Z` |
| `sys_log_level` | `"INFO"` | `system` | 1 | `2025-11-02T10:07:00Z` |

## Version Upgrade

After adding the new entries, set the `version` field to `2` for **every** entry in the store (all 18 entries).

## Output

Write the updated store back to `setup/store.json`. It should contain 18 entries, all with version 2.
