# Challenge 045: Write Unit Tests

## Difficulty: Easy

## Task

The file `setup/utils.py` contains a complete, working utility module with several functions. Your job is to write comprehensive unit tests for every function.

## Functions to Test

1. `slugify(text) -> str` — Converts text to a URL-friendly slug (lowercase, hyphens instead of spaces, no special chars)
2. `truncate(text, max_len, suffix="...") -> str` — Truncates text to max_len characters, appending suffix if truncated
3. `is_valid_url(url) -> bool` — Returns True if the string is a valid HTTP/HTTPS URL
4. `deep_merge(dict_a, dict_b) -> dict` — Deep merges two dictionaries, with dict_b values taking precedence
5. `chunk_list(lst, size) -> list` — Splits a list into chunks of the given size

## Rules

- Only modify files in the `setup/` directory
- Write your tests in `setup/test_utils.py`
- You must write at least 10 test functions
- Each function in utils.py should have at least 2 tests
- Tests should cover both normal cases and edge cases

## Examples

```python
slugify("Hello World!")          # "hello-world"
truncate("Hello, World!", 8)     # "Hello..."
is_valid_url("https://x.com")   # True
deep_merge({"a": 1}, {"b": 2})  # {"a": 1, "b": 2}
chunk_list([1,2,3,4,5], 2)      # [[1,2], [3,4], [5]]
```
