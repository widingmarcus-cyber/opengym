# Challenge 091: Build File Index

## Difficulty: Medium

## Task

The file `setup/indexer.py` contains a stub. Implement a function that recursively indexes a directory and produces a comprehensive summary including duplicate detection.

## Requirements

1. `index_directory(path) -> dict` -- Recursively scan the directory at `path` and return a dictionary with the following keys:

   - `total_files` (int): Total number of files found (not directories).
   - `total_size` (int): Sum of all file sizes in bytes.
   - `file_types` (dict): Mapping of file extension (including the dot, e.g. `".py"`) to the count of files with that extension. Files with no extension use the key `""`.
   - `largest_files` (list): Top 5 files by size, as a list of `(path_str, size)` tuples sorted descending by size. Paths should be relative to the indexed directory.
   - `duplicate_groups` (list): A list of groups where each group is a sorted list of relative paths that have identical content (same MD5 or SHA256 hash). Only include groups with 2+ files. Sort groups by the first path in each group.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.

## Example

```python
result = index_directory("sample_tree/")
result["total_files"]       # 20
result["file_types"]        # {".py": 5, ".txt": 3, ".csv": 2, ...}
result["largest_files"]     # [("data/big.csv", 10240), ("src/main.py", 2048), ...]
result["duplicate_groups"]  # [["docs/copy1.txt", "docs/copy2.txt"], ...]
```
