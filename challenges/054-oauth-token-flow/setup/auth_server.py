import uuid


class AuthServer:
    """Simulated OAuth2 authorization server."""

    def __init__(self, valid_clients=None, token_ttl=3600):
        self._valid_clients = valid_clients or {}
        self._token_ttl = token_ttl
        self._active_tokens = set()

    def token(self, client_id, client_secret):
        """Issue an access token for valid client credentials."""
        if self._valid_clients.get(client_id) != client_secret:
            raise ValueError("Invalid client credentials")

        access_token = f"tok_{uuid.uuid4().hex[:16]}"
        self._active_tokens.add(access_token)
        return {
            "access_token": access_token,
            "expires_in": self._token_ttl,
        }

    def validate(self, token):
        """Check if a token is currently active on the server."""
        return token in self._active_tokens

    def revoke_token(self, token):
        """Revoke an active token."""
        self._active_tokens.discard(token)
