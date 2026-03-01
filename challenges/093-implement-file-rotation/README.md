# Challenge 093: Implement File Rotation

## Difficulty: Hard

## Task

The file `setup/rotator.py` contains a stub. Implement a `FileRotator` class that manages log file rotation with automatic size-based rotation, timestamped archives, and cleanup of old files.

## Requirements

1. `FileRotator(base_path, max_files=5, max_size_bytes=1048576)` -- Constructor. `base_path` is the path to the main log file (e.g., `"app.log"`). `max_files` is the maximum number of archived files to keep. `max_size_bytes` is the threshold that triggers rotation.

2. `write(content)` -- Append `content` (a string) to the current log file. If writing would cause the file to exceed `max_size_bytes`, call `rotate()` first, then write to the new (empty) file.

3. `rotate()` -- Archive the current log file by renaming it with a timestamp suffix in the format `base.log.YYYY-MM-DD-HHMMSS`. After rotation, the original `base_path` should be empty (or not exist) and ready for new writes. If there is nothing to rotate (file is empty or does not exist), do nothing.

4. `cleanup()` -- Remove the oldest archived files so that at most `max_files` archived files remain. Archived files are sorted by their timestamp suffix.

5. `get_archived_files() -> list` -- Return a sorted list of paths to all archived files (oldest first).

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.
- Tests will use temporary directories.

## Example

```python
rotator = FileRotator("/tmp/app.log", max_files=3, max_size_bytes=100)
rotator.write("First log entry\n")
rotator.write("x" * 200)  # triggers auto-rotation
archived = rotator.get_archived_files()
# ["/tmp/app.log.2024-01-15-103000"]
```
