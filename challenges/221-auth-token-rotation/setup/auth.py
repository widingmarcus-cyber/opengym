"""
Authentication token management module.
VULNERABILITY: Uses a static hardcoded token that never rotates.
If the token is compromised, an attacker has indefinite access.
"""


HARDCODED_TOKEN = "static-secret-token-12345-never-changes"


class TokenManager:
    """
    Manages authentication tokens.
    Currently uses a hardcoded static token with no rotation.
    """

    def __init__(self):
        # BUG: Hardcoded static token
        self.token = HARDCODED_TOKEN

    def get_current_token(self):
        """Return the current valid token."""
        return self.token

    def authenticate(self, token):
        """
        Verify if the provided token is valid.

        Args:
            token: The token string to verify.

        Returns:
            dict with "status" ("ok" or "denied") and "message"
        """
        # BUG: Only checks against static token
        if token == self.token:
            return {"status": "ok", "message": "Authentication successful"}
        return {"status": "denied", "message": "Invalid token"}

    def rotate_token(self):
        """
        Generate a new token and invalidate the old one.

        Returns:
            The new token string.
        """
        # BUG: Does nothing — token never changes
        return self.token
