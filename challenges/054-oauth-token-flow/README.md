# Challenge 054: OAuth Token Flow

## Difficulty: Hard

## Task

Implement an OAuth2 client-credentials flow client. The file `setup/oauth_client.py` contains a stub that needs to be completed.

## Setup

`setup/auth_server.py` provides a simulated `AuthServer` class:
- `token(client_id, client_secret)` — Returns `{"access_token": str, "expires_in": int}` if credentials are valid, raises `ValueError` otherwise
- `validate(token)` — Returns `True` if the token is currently valid, `False` otherwise
- `revoke_token(token)` — Revokes the given token

## Requirements

Implement an `OAuthClient` class in `setup/oauth_client.py`:

### Constructor

`OAuthClient(server, client_id, client_secret, time_fn=None)` — Takes the auth server, credentials, and an optional time function for testing.

### Methods

1. `authenticate()` — Obtain a new access token from the server. Raises `ValueError` if credentials are invalid.
2. `get_token()` — Return the current access token. If no token exists or the token has expired, automatically authenticate to get a fresh one. Returns the token string.
3. `is_authenticated()` — Return `True` if the client has a valid (non-expired) token, `False` otherwise.
4. `revoke()` — Revoke the current token on the server and clear local token state. Does nothing if not authenticated.

## Rules

- Only modify files in the `setup/` directory (do not modify `auth_server.py`)
- Token expiry should be tracked using `time_fn` for deterministic testing
- Expired tokens should be automatically refreshed on `get_token()`
