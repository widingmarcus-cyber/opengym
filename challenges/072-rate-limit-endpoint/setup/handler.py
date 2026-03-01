"""Request handler with no rate limiting."""


def handle_request(client_id, request, time_fn=None):
    """Handle an API request.

    Args:
        client_id: Identifier for the client making the request.
        request: Dictionary containing the request data.
        time_fn: Optional callable returning current time as float.

    Returns:
        A response dictionary.
    """
    result = process(request)
    return {"status": "ok", "data": result}


def process(request):
    """Process a request and return result data."""
    return {"received": request.get("action", "unknown")}
