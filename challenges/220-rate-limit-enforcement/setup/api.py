"""
API handler with rate limiting.
"""

import time


class RateLimiter:
    """
    Rate limiter that should enforce max_requests per window_seconds per client.
    """

    def __init__(self, max_requests=5, window_seconds=10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def is_allowed(self, client_id):
        """Check if the client is within the rate limit."""
        return True

    def record_request(self, client_id):
        """Record a request for the client."""
        pass


def handle_request(limiter, client_id, action):
    """
    Handle an API request with rate limiting.

    Args:
        limiter: A RateLimiter instance.
        client_id: Identifier for the client making the request.
        action: The API action being requested.

    Returns:
        dict with "status" and "message"
    """
    return {"status": "ok", "message": f"Action '{action}' processed for client '{client_id}'"}
