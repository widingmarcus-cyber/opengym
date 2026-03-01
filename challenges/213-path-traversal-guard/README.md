# Challenge 213: Path Traversal Guard

## Objective

Fix a file server that is vulnerable to **path traversal attacks**. The server currently allows requests like `../../etc/passwd` to escape the designated `files/` directory and read arbitrary files on the system.

## Setup

- `setup/server.py` — A simple file-serving module with a `serve_file(base_dir, requested_path)` function.
- `setup/files/` — The allowed directory containing `hello.txt` and `readme.txt`.

## What You Must Do

1. Open `setup/server.py` and find the `serve_file` function.
2. The function naively joins the base directory with the user-supplied path. This allows path traversal (e.g., `../../../etc/passwd`).
3. Patch the function so that:
   - Legitimate file requests within `files/` still work (e.g., `hello.txt` returns its content).
   - Any request that would resolve outside the base directory is rejected with an error.
   - Both `../` sequences and absolute paths are blocked.
4. The function should return a dict: `{"status": "ok", "content": "..."}` on success, or `{"status": "error", "message": "..."}` on rejection.

## Constraints

- Do NOT change the function signature.
- Do NOT remove or rename existing files in `setup/files/`.
- The fix must handle edge cases: encoded traversals, null bytes, absolute paths.
