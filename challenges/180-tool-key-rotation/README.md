# Challenge 180: Tool Key Rotation

## Objective

Handle API key rotation by detecting a 403 error indicating key rotation and switching to the updated key.

## Scenario

You have access to `tools/secure_api.py`, a secure API that requires an API key. The current key has been rotated and will return a 403 error. The rotated (new) key is available in the same configuration file.

## Instructions

1. Read `setup/keys.json` to get the current API key.
2. Call `tools/secure_api.py --api-key <current_key>`.
3. If you receive a 403 status with a rotation message, read the `rotated` key from `setup/keys.json`.
4. Retry the API call with the rotated key.
5. Write the `data` value from the successful response to `setup/answer.txt`.

## Tools

- `tools/secure_api.py --api-key <key>` - Makes a secure API call with the given key.

## Expected Output

- `setup/answer.txt` containing the data value.
