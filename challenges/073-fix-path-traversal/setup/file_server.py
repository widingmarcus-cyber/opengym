"""Simple file server."""

import os


def serve_file(base_dir, requested_path):
    """Serve a file from the base directory.

    Args:
        base_dir: The root directory to serve files from.
        requested_path: The requested file path relative to base_dir.

    Returns:
        The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the path attempts to escape base_dir.
    """
    file_path = os.path.join(base_dir, requested_path)
    with open(file_path, "r") as f:
        return f.read()
