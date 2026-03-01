# Challenge 011: Fix the Type Errors

## Difficulty: Easy

## Task

The file `setup/registration.py` contains a user registration module with several functions. Each function has a type-related bug -- for example, concatenating incompatible types, passing the wrong type to a built-in, or returning the wrong type.

**Your job:** Fix all type errors so the module works correctly.

## Functions

1. `create_username(first_name, last_name, year_of_birth)` -- Builds a username string like "john_doe_1990"
2. `build_profile(name, age, tags)` -- Returns a dict with user profile info, including a sorted copy of the tags list
3. `format_address(street, city, zip_code)` -- Formats an address string from components
4. `calculate_age_in_months(age_years)` -- Returns the age converted to months as an integer
5. `merge_preferences(defaults, overrides)` -- Merges two preference dicts, with overrides taking priority

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures (names, parameters)
- The functions should work as their names and docstrings suggest
