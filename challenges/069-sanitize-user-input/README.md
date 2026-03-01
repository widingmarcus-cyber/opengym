# Challenge 069: Sanitize User Input

## Difficulty: Easy

## Task

The file `setup/renderer.py` contains a `render_template` function that uses Python's `str.format()` to insert user data into templates. This is vulnerable to format string injection attacks.

Fix the function to safely render templates without allowing users to access internal Python object attributes or other variables.

## Setup

- `setup/renderer.py` — Contains the vulnerable `render_template` function

## Requirements

Fix `render_template(template, user_data)` so that:

1. Normal rendering still works (e.g., `{name}` is replaced with the user's name)
2. Format string injection attacks are prevented (e.g., `{name.__class__}`, `{balance.__format__}`)
3. Users cannot access attributes of inserted values through format string syntax
4. The function should either sanitize/escape dangerous patterns or use a safe rendering approach

## Rules

- Only modify `setup/renderer.py`
- The function signature must remain `render_template(template, user_data)`
- Normal template rendering with simple `{key}` placeholders must still work
