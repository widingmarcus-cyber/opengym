"""
API handler with rate limiting.
VULNERABILITY: The RateLimiter is a stub that always allows requests,
making the API vulnerable to abuse and denial-of-service.
"""

import time


class RateLimiter:
    """
    Rate limiter that should enforce max_requests per window_seconds per client.
    Currently a stub that always allows requests.
    """

    def __init__(self, max_requests=5, window_seconds=10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # BUG: No storage for tracking requests

    def is_allowed(self, client_id):
        """Check if the client is within the rate limit."""
        # BUG: Always returns True — no rate limiting
        return True

    def record_request(self, client_id):
        """Record a request for the client."""
        # BUG: Does nothing — no request tracking
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
    # BUG: Does not check rate limiter before processing
    return {"status": "ok", "message": f"Action '{action}' processed for client '{client_id}'"}
