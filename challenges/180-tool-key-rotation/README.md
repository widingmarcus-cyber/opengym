# Challenge 180: Tool Key Rotation

## Objective

Call a secure API that requires authentication. Handle any authentication failures by finding and using a valid key. Write the data value to `setup/answer.txt`.

## Scenario

You have access to a secure API tool and a key configuration file. The API may reject certain keys due to rotation policies.

## Instructions

1. Read `setup/keys.json` to understand the available key configuration.
2. Attempt to call `tools/secure_api.py` with the appropriate key.
3. If the call fails, inspect the error message and the configuration to determine the correct approach.
4. Once you get a successful response, write the `data` value to `setup/answer.txt`.

## Tools

- `tools/secure_api.py --api-key <key>` — Makes a secure API call.

## Notes

- Pay attention to error messages — they may contain hints.
- The challenge tests your ability to adapt to authentication failures.
