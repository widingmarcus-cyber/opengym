# Challenge 215: Symlink Escape

## Objective

Fix a file processor that **follows symlinks** outside of its allowed directory. The processor reads files from a `data/` directory, but an attacker could create symlinks that point to files outside that directory (e.g., `/etc/shadow`, private keys).

## Setup

- `setup/processor.py` — A module with a `process_files(data_dir)` function that reads all files in a directory and returns their contents.
- `setup/data/` — The allowed data directory containing `report.txt` and `notes.txt`.

## What You Must Do

1. Open `setup/processor.py` and find the `process_files` function.
2. The function currently reads every file in the directory without checking whether any entry is a symlink pointing outside the allowed directory.
3. Fix the function so that:
   - Regular files within `data/` are read normally.
   - Symlinks that resolve to targets **outside** the `data/` directory are skipped with an error entry.
   - Symlinks that resolve to targets **within** the `data/` directory are still allowed.
4. The function returns a dict mapping filenames to either `{"status": "ok", "content": "..."}` or `{"status": "error", "message": "..."}`.

## Constraints

- Do NOT change the function signature.
- Do NOT remove existing files in `setup/data/`.
- The fix must use `os.path.realpath()` to resolve symlinks before checking boundaries.
