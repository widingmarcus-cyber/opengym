# Challenge 179: Tool Auth Refresh

## Objective

Handle expired authentication tokens by detecting 401 errors, refreshing the token, and retrying the request.

## Scenario

You have access to `tools/auth_api.py`, an API tool that requires a valid token. The current token in `setup/token.txt` has expired. You must detect the expiration, refresh the token, and use the new token to retrieve the data.

## Instructions

1. Read the current token from `setup/token.txt`.
2. Call `tools/auth_api.py --token <token>` with the token from the file.
3. If you receive a 401 status ("Token expired"), refresh the token by calling `tools/auth_api.py --refresh`.
4. Use the `new_token` from the refresh response to make another API call.
5. Write the `data` value from the successful response to `setup/answer.txt`.
6. Update `setup/token.txt` with the new token.

## Tools

- `tools/auth_api.py --token <token>` - Makes an authenticated API call.
- `tools/auth_api.py --refresh` - Refreshes the token and returns a new one.

## Expected Output

- `setup/answer.txt` containing the data value.
- `setup/token.txt` updated with the fresh token.
