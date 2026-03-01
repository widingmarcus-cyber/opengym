# Challenge 232: Canonical JSON Output

## Objective

Produce a canonical (deterministic, byte-identical) JSON representation of input data.

## Context

JSON does not define key ordering, whitespace, or number formatting. This means two JSON serializations of the same data can produce different bytes, breaking checksums, diffs, and caching. Canonical JSON solves this by enforcing strict rules: sorted keys, consistent formatting, no trailing whitespace, and stable number representations.

## Task

Read `setup/data.json` which contains a complex nested JSON object with various data types. Write a Python script `setup/canonicalize.py` that reads `data.json` and writes `setup/canonical.json` following these canonical rules:

1. **Sorted keys**: All object keys must be sorted lexicographically (recursively, at all nesting levels)
2. **Indentation**: 2-space indentation
3. **No trailing whitespace** on any line
4. **Numbers**: No unnecessary floating point drift — integers stay as integers (e.g., `42` not `42.0`), floats use minimal representation
5. **Strings**: Use standard JSON escaping, no unnecessary Unicode escapes
6. **File ending**: Single trailing newline (`\n`) at end of file
7. **Separator**: No trailing spaces after colons or commas (`": "` between key-value, no space before colon)

Running `python3 setup/canonicalize.py` multiple times must produce a byte-identical `setup/canonical.json` every time.

## Requirements

- Create `setup/canonicalize.py` that reads `data.json` and writes `canonical.json`
- Output must follow all canonical rules above
- Running the script multiple times must produce byte-identical output
- All data from the input must be preserved (no data loss)
- The script must be executable: `python3 setup/canonicalize.py`

## Verification

```bash
python3 tests/verify.py
```
