# Challenge 074: Secure Deserialization

## Difficulty: Hard

## Task

The file `setup/storage.py` uses Python's `pickle` module for serialization and deserialization. While functional, `pickle` is inherently insecure because it can execute arbitrary code during deserialization.

Replace the pickle-based implementation with a safe JSON-based approach that handles common Python types.

## Setup

- `setup/storage.py` — Contains `save(data, filepath)` and `load(filepath)` using pickle

## Requirements

Replace the pickle-based serialization with safe JSON-based serialization that:

1. Handles standard JSON types (str, int, float, bool, None, list, dict)
2. Handles `datetime` objects (serialize to ISO format string, deserialize back)
3. Handles `set` objects (serialize as a list with a type marker, deserialize back to set)
4. Handles `bytes` objects (serialize as base64 with a type marker, deserialize back)
5. Handles custom class instances by converting them to dicts (via `__dict__`)
6. Does NOT use `pickle` anywhere
7. Rejects (raises an error) when asked to load a pickle file

## Rules

- Only modify `setup/storage.py`
- The function signatures must remain `save(data, filepath)` and `load(filepath)`
- Use `.json` extension for saved files
- Raise `ValueError` if a pickle file is detected during `load()`
