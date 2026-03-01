# Step 1: Write Data and Compute Checksum

1. Write the following JSON object to `setup/data.json`:

```json
{"records": [{"id": 1, "value": "alpha"}, {"id": 2, "value": "beta"}, {"id": 3, "value": "gamma"}]}
```

2. Compute the SHA-256 hash of the exact file contents of `setup/data.json` (the raw bytes of the file).

3. Write the hex-encoded SHA-256 digest to `setup/checksum.txt` (just the hash string, no extra whitespace or newlines).

Both `setup/data.json` and `setup/checksum.txt` will persist to the next session.
