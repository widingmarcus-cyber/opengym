# Challenge 005: Fix the Logic Bug

## Difficulty: Medium

## Task

The file `setup/validators.py` contains input validation functions. They all have logic bugs — they return wrong results for certain edge cases.

**Your job:** Fix the logic in each function so all edge cases are handled correctly.

## Functions

1. `is_valid_email(email)` — Returns `True` if the email has a valid basic format (contains exactly one `@`, has text before and after `@`, part after `@` contains a `.`)
2. `is_palindrome(s)` — Returns `True` if the string is a palindrome (case-insensitive, ignoring spaces and punctuation)
3. `is_valid_password(password)` — Returns `True` if password has: at least 8 chars, at least one uppercase, at least one lowercase, at least one digit
4. `flatten_list(nested)` — Takes a nested list and returns a flat list of all values

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- Read the current implementation carefully — the bugs are subtle
