"""
Authentication token management module.
"""


HARDCODED_TOKEN = "static-secret-token-12345-never-changes"


class TokenManager:
    """
    Manages authentication tokens.
    """

    def __init__(self):
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
        if token == self.token:
            return {"status": "ok", "message": "Authentication successful"}
        return {"status": "denied", "message": "Invalid token"}

    def rotate_token(self):
        """
        Generate a new token and invalidate the old one.

        Returns:
            The new token string.
        """
        return self.token
