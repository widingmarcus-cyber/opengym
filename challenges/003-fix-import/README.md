# Challenge 003: Fix the Import

## Difficulty: Easy

## Task

The project in `setup/` has a small package with two modules, but the imports are broken. The main script `setup/main.py` tries to use functions from the `utils` package but fails with ImportError.

**Your job:** Fix the import statements so `main.py` runs correctly.

## Project Structure

```
setup/
├── main.py          # Entry point — fix imports here
└── utils/
    ├── __init__.py
    ├── strings.py   # String utilities
    └── math.py      # Math utilities
```

## Rules

- Only modify files in the `setup/` directory
- Do not change function implementations, only fix imports
- All functions should be importable from where `main.py` expects them

## Expected Behavior

When `main.py` runs, it should:
1. Successfully import `reverse_string` and `capitalize_words` from utils
2. Successfully import `clamp` and `average` from utils
3. Produce correct output for the test calls
