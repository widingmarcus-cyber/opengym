# Challenge 150: Lock Timeout

**Difficulty:** Hard
**Category:** shared-resources
**Dimension:** multi-agent
**Type:** Multi-session (2 steps)

## Objective

Handle a stale lock that has been held far past its timeout. Detect the stale lock, force-release it, acquire it yourself, perform the operation, and release cleanly.

## What This Tests

- Detecting stale/expired locks based on timestamp and timeout
- Force-releasing locks that have exceeded their timeout
- Proper lock lifecycle after recovery
- Writing to a resource after lock recovery

## Sessions

1. **Recovery Agent** -- `setup/lock.json` is pre-loaded with a stale lock held by `"stale_process"` since `"2024-01-01T00:00:00Z"`. The timeout is 60 seconds. Detect that the lock has been held for over 24 hours, force-release it, acquire it yourself, write `"RECOVERED"` to `setup/result.txt`, then release the lock.
2. **Verifier** -- Read `setup/result.txt` and `setup/lock.json`. If result.txt says `"RECOVERED"` and the lock is released, write `"LOCK_RECOVERED"` to `setup/answer.txt`.

## Constraints

- `setup/lock.json` is pre-created with `{"locked": true, "holder": "stale_process", "acquired_at": "2024-01-01T00:00:00Z"}`.
- `setup/result.txt` must contain `"RECOVERED"`.
- `setup/lock.json` must have `"locked": false` after step 1 (lock released).
- `setup/answer.txt` must contain `"LOCK_RECOVERED"`.
