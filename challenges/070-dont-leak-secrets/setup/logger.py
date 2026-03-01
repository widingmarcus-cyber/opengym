"""HTTP request logger."""


def log_request(method, url, headers, body):
    """Log an HTTP request with all its details.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Request URL string.
        headers: Dictionary of HTTP headers.
        body: Dictionary of request body parameters.

    Returns:
        The formatted log string.
    """
    header_str = ", ".join(f"{k}: {v}" for k, v in headers.items())
    body_str = ", ".join(f"{k}={v}" for k, v in body.items()) if body else ""

    log = f"{method} {url} | Headers: {header_str} | Body: {body_str}"
    return log
