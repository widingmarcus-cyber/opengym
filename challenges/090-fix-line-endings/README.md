# Challenge 090: Fix Line Endings

## Difficulty: Easy

## Task

The file `setup/line_endings.py` contains stubs. Implement functions to detect, normalize, and fix line endings in text and files.

## Requirements

1. `normalize_endings(text, ending="\n") -> str` -- Convert all line endings in `text` to the specified `ending`. Must handle `\r\n` (CRLF), `\r` (CR), and `\n` (LF). The `ending` parameter can be `"\n"`, `"\r\n"`, or `"\r"`.

2. `detect_endings(text) -> str` -- Detect the type of line endings in `text`. Return `"lf"` if all line endings are `\n`, `"crlf"` if all are `\r\n`, `"cr"` if all are `\r`, or `"mixed"` if the text contains more than one type. Return `"none"` if the text has no line endings.

3. `fix_file(filepath, ending="\n")` -- Read the file at `filepath` in binary mode, normalize its line endings, and write the result back. The file should be read and written in binary mode to preserve exact byte content.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.

## Example

```python
normalize_endings("hello\r\nworld\nfoo\r\n", "\n")
# "hello\nworld\nfoo\n"

detect_endings("hello\r\nworld\r\n")
# "crlf"

detect_endings("line1\nline2\r\nline3\n")
# "mixed"
```
