# Challenge 221: Auth Token Rotation

## Objective

Implement **authentication token rotation** in an auth module that currently uses static, hardcoded tokens. Static tokens are a security risk because if compromised, they grant indefinite access.

## Setup

- `setup/auth.py` — An authentication module with:
  - A `TokenManager` class that manages auth tokens.
  - Currently uses a hardcoded static token that never changes.
  - `authenticate(token)` — Verifies a token.
  - `get_current_token()` — Returns the current valid token.
  - `rotate_token()` — Should generate a new token and invalidate the old one (currently a no-op).

## What You Must Do

1. Implement `rotate_token()` to:
   - Generate a new cryptographically random token (use `secrets.token_hex(32)` or similar).
   - Store the new token as the current token.
   - Keep the previous token valid for a grace period (to handle in-flight requests). The previous token should be stored separately.
   - Return the new token.
2. Update `authenticate(token)` to:
   - Accept both the current token AND the previous token (grace period).
   - Reject all other tokens.
   - Reject the hardcoded initial token after the first rotation.
3. Update `get_current_token()` to return the current (most recently generated) token.
4. The initial token must be replaced on first `rotate_token()` call.

## Constraints

- Do NOT change function signatures.
- Tokens must be generated using the `secrets` module (cryptographically secure).
- The `authenticate` method must accept both current and previous tokens (grace period).
- After rotation, the OLD old token (two rotations ago) must be rejected.
