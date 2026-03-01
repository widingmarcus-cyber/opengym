"""
File processor module.
VULNERABILITY: The process_files function follows symlinks without validation,
allowing an attacker to read files outside the allowed data directory by
placing symlinks inside it.
"""

import os


def process_files(data_dir):
    """
    Read all files in data_dir and return their contents.

    Args:
        data_dir: Path to the directory containing data files.

    Returns:
        dict mapping filename to {"status": "ok", "content": "..."} or
        {"status": "error", "message": "..."}
    """
    results = {}
    data_dir = os.path.abspath(data_dir)

    if not os.path.isdir(data_dir):
        return {"__error__": {"status": "error", "message": "Data directory not found"}}

    for entry in os.listdir(data_dir):
        entry_path = os.path.join(data_dir, entry)

        # BUG: No symlink validation — blindly reads whatever the path resolves to
        if os.path.isfile(entry_path):
            try:
                with open(entry_path, "r") as f:
                    content = f.read()
                results[entry] = {"status": "ok", "content": content}
            except Exception as e:
                results[entry] = {"status": "error", "message": str(e)}

    return results
