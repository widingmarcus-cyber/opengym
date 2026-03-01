# Challenge 073: Fix Path Traversal

## Difficulty: Hard

## Task

The file `setup/file_server.py` contains a `serve_file` function that serves files from a base directory. It is vulnerable to path traversal attacks that allow reading arbitrary files on the system.

Fix the function to prevent path traversal while still serving valid files.

## Setup

- `setup/file_server.py` — Contains the vulnerable file-serving function

## Requirements

Fix `serve_file(base_dir, requested_path)` so that:

1. Valid file paths within the base directory are served correctly
2. Path traversal attempts (e.g., `../../etc/passwd`) are rejected
3. URL-encoded traversal attempts (e.g., `%2e%2e%2f`) are rejected
4. The function raises `PermissionError` when a traversal attempt is detected
5. The resolved path must be strictly within the base directory
6. Paths with redundant separators or dots are handled safely

## Rules

- Only modify `setup/file_server.py`
- The function signature must remain `serve_file(base_dir, requested_path)`
- Return file contents as a string for valid paths
- Raise `FileNotFoundError` if the file doesn't exist (within the base directory)
- Raise `PermissionError` for traversal attempts
