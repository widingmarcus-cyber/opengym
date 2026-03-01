# Step 1: Verify Data Integrity

You have three files in `setup/`:

- `setup/data.json` — the data file to verify
- `setup/data.checksum` — the expected SHA-256 hash of the original (untampered) data
- `setup/backup.json` — a known-good backup of the original data

Your task:

1. Read `setup/data.json` and compute its SHA-256 hash (hash the raw file contents as UTF-8 bytes).
2. Read `setup/data.checksum` to get the expected hash.
3. Compare the two hashes.
4. If they do NOT match, the data has been corrupted. Write `CORRUPTED` to `setup/status.txt`.
5. If they match, write `VALID` to `setup/status.txt`.

Note: The data file has been tampered with -- one value was changed from the original.
