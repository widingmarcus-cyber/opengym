# Challenge 182: Tool Response Checksum

## Objective

Verify the integrity of a tool's response by validating its checksum before trusting the data.

## Scenario

You have access to `tools/verified_api.py`, a tool that returns data along with a SHA-256 checksum for integrity verification. Your job is to call the tool, verify the checksum matches the data, and only write the data if the checksum is valid.

## Instructions

1. Call `tools/verified_api.py` (no arguments needed).
2. The response contains `data` and `checksum` fields.
3. Compute the SHA-256 hex digest of the `data` string.
4. Compare your computed checksum with the one in the response.
5. If they match, write the `data` value to `setup/answer.txt`.
6. If they do NOT match, write `CHECKSUM_MISMATCH` to `setup/answer.txt`.

## Tools

- `tools/verified_api.py` - Returns data with a SHA-256 checksum for verification.

## Expected Output

- `setup/answer.txt` containing the verified data value (or "CHECKSUM_MISMATCH" if invalid).
