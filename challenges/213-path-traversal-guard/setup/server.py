"""
Simple file server module.
"""

import os


def serve_file(base_dir, requested_path):
    """
    Serve a file from base_dir based on the requested_path.

    Returns:
        dict with "status" and either "content" or "message"
    """
    file_path = os.path.join(base_dir, requested_path)

    if not os.path.isfile(file_path):
        return {"status": "error", "message": "File not found"}

    with open(file_path, "r") as f:
        content = f.read()

    return {"status": "ok", "content": content}
