# Challenge 175: Tool Unavailable

## Objective

Try the primary tool. When it reports being unavailable, fall back to the backup tool. Write the backup result to `setup/answer.txt`.

## Context

Services go down for maintenance, experience outages, or get deprecated. A robust agent must detect when a primary tool is unavailable and seamlessly switch to a backup or alternative tool rather than failing entirely.

## Tools

- `tools/primary.py` — Primary service (currently down for maintenance). Always returns unavailable status.
- `tools/backup.py` — Backup service. Always returns successfully.

## Instructions

1. Call `tools/primary.py` to attempt the primary service.
2. The primary service will return `{"status": "unavailable", "error": "Service is down for maintenance"}`.
3. Detect the unavailable status.
4. Call `tools/backup.py` as a fallback.
5. Extract the `data` value from the backup response.
6. Write it to `setup/answer.txt`.

## Expected Behavior

- `tools/primary.py` always returns unavailable.
- `tools/backup.py` returns `{"status": "ok", "data": "backup_result_77"}`.
- `setup/answer.txt` should contain: `backup_result_77`
