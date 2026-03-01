# Step 2: Verify Data Integrity

1. Read the contents of `setup/data.json`.
2. Read the stored checksum from `setup/checksum.txt`.
3. Recompute the SHA-256 hash of the exact file contents of `setup/data.json`.
4. Compare the recomputed hash with the stored checksum.
5. If they match, write `VALID` to `setup/status.txt`.
6. If they do not match, write `INVALID` to `setup/status.txt`.

Write only the word `VALID` or `INVALID` with no extra text or formatting.
