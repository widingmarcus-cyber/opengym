# Challenge 025: Write Diff Tool

## Difficulty: Hard

## Task

The file `setup/differ.py` is empty. Implement a line-by-line diff tool that compares two texts and produces structured and unified diff output.

## Requirements

### DiffLine dataclass

A dataclass with:
- `type` — One of `"equal"`, `"added"`, `"removed"`
- `content` — The text content of the line (without newline)

### Functions

1. `diff(text_a, text_b)` — Compare two strings line-by-line. Return a list of `DiffLine` objects representing the differences. Use a longest common subsequence (LCS) approach for accurate results
2. `unified_diff(text_a, text_b)` — Return a string in unified diff format where:
   - Equal lines are prefixed with `" "` (space)
   - Added lines are prefixed with `"+"`
   - Removed lines are prefixed with `"-"`
   - Lines are joined with newlines

## Rules

- Only modify files in the `setup/` directory
- Handle edge cases: empty strings, identical inputs, completely different inputs
- Split text on newline characters (`"\n"`)

## Examples

```python
a = "hello\nworld"
b = "hello\nearth"

result = diff(a, b)
# [DiffLine("equal", "hello"), DiffLine("removed", "world"), DiffLine("added", "earth")]

print(unified_diff(a, b))
#  hello
# -world
# +earth
```
