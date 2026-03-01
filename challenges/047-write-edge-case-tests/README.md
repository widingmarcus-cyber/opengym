# Challenge 047: Write Edge Case Tests

## Difficulty: Medium

## Task

The file `setup/string_utils.py` contains a working string utility module. Your job is to write tests that thoroughly cover edge cases and boundary conditions for every function.

## Functions to Test

1. `wrap_text(text, width)` — Word-wraps text to the given width. Splits on spaces, preserving words when possible. If a single word exceeds the width, it is placed on its own line.
2. `pad_center(text, width, char=" ")` — Centers text within the given width using the padding character. If text is longer than width, returns text unchanged.
3. `remove_duplicates(text)` — Removes consecutive duplicate characters (e.g., "aabbc" -> "abc").
4. `count_words(text)` — Counts the number of words in text, where words are separated by whitespace.

## Edge Cases to Consider

- Empty strings
- Single character strings
- Width of 0 or 1
- Text that is exactly the width
- Text shorter than the width
- Unicode characters
- Strings with only whitespace
- Very long single words

## Rules

- Only modify files in the `setup/` directory
- Write your tests in `setup/test_edge_cases.py`
- You must write at least 12 test functions
- Each function should have edge case tests

## Examples

```python
wrap_text("hello world", 5)       # "hello\nworld"
pad_center("hi", 6)               # "  hi  "
remove_duplicates("aaabbbccc")    # "abc"
count_words("  hello   world  ")  # 2
```
