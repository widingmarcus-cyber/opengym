"""
Simple file server module.
VULNERABILITY: The serve_file function does not validate that the requested
path stays within the base directory. An attacker can use path traversal
sequences like ../../ to read arbitrary files.
"""

import os


def serve_file(base_dir, requested_path):
    """
    Serve a file from base_dir based on the requested_path.

    Returns:
        dict with "status" and either "content" or "message"
    """
    # BUG: No validation — path traversal is possible
    file_path = os.path.join(base_dir, requested_path)

    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    with open(file_path, "r") as f:
        content = f.read()

    return {"status": "ok", "content": content}
