# Challenge 012: Fix the Encoding Bug

## Difficulty: Medium

## Task

The file `setup/text_processor.py` is a text-processing script that reads a file and performs various operations on its content. However, it crashes or produces wrong results when the text contains emoji, accented characters, or other non-ASCII Unicode content.

A sample input file `setup/sample.txt` is provided with emoji and accented characters.

**Your job:** Fix the encoding and text-processing bugs so the module handles all Unicode text correctly.

## Functions

1. `read_file(filepath)` -- Reads a text file and returns its contents as a string
2. `count_characters(text)` -- Returns the number of characters in the text (not bytes)
3. `reverse_text(text)` -- Returns the text reversed character-by-character
4. `extract_words(text)` -- Splits text into a list of words (whitespace-separated), stripping punctuation from each word
5. `truncate(text, max_chars)` -- Truncates text to max_chars characters, appending "..." if truncated

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- All functions must handle Unicode text (emoji, accented characters, CJK, etc.) correctly
