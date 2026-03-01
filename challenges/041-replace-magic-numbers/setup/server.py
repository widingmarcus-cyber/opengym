"""Server configuration utilities."""


def validate_port(port):
    """Check if a port number is valid."""
    if not isinstance(port, int):
        raise TypeError("port must be an integer")
    if port < 1 or port > 65535:
        raise ValueError(f"port must be between 1 and 65535, got {port}")
    return port


def create_config(host="localhost", port=None, timeout=None, retries=None):
    """Create a server configuration dict."""
    if port is None:
        port = 8080
    if timeout is None:
        timeout = 30
    if retries is None:
        retries = 3

    validate_port(port)

    return {
        "host": host,
        "port": port,
        "timeout": timeout,
        "retries": retries,
        "buffer_size": 4096,
        "max_connections": 100,
    }


def allocate_buffer(count=1):
    """Allocate buffer space. Returns total bytes allocated."""
    if count < 1:
        raise ValueError("count must be at least 1")
    return count * 4096


def check_connections(current):
    """Check if we can accept more connections."""
    if current >= 100:
        return {"accept": False, "remaining": 0, "message": "at capacity"}
    return {
        "accept": True,
        "remaining": 100 - current,
        "message": f"{100 - current} slots available",
    }


def retry_request(func):
    """Retry a function up to the max retry limit. Returns (success, result)."""
    last_error = None
    for attempt in range(3):
        try:
            result = func()
            return True, result
        except Exception as e:
            last_error = e
    return False, str(last_error)


def get_server_defaults():
    """Return a dict of all server default values."""
    return {
        "port": 8080,
        "timeout": 30,
        "retries": 3,
        "buffer_size": 4096,
        "max_connections": 100,
        "max_port": 65535,
    }
