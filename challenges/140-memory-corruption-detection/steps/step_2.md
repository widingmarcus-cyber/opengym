# Step 2: Restore from Backup

In the previous step, you detected that `setup/data.json` was corrupted (its hash did not match `setup/data.checksum`).

Your task:

1. Copy the contents of `setup/backup.json` to `setup/data.json`, replacing the corrupted file.
2. Recompute the SHA-256 hash of the restored `setup/data.json` (hash the raw file contents as UTF-8 bytes).
3. Write the new hash to `setup/data.checksum`.
4. Write `RESTORED` to `setup/status.txt`.

After this step, `setup/data.json` should be identical to `setup/backup.json`, and `setup/data.checksum` should match the actual SHA-256 of `setup/data.json`.
