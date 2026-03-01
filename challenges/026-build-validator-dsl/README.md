# Challenge 026: Build Validator DSL

## Difficulty: Hard

## Task

The file `setup/validator.py` is empty. Implement a declarative validation system using a schema DSL (domain-specific language).

## Requirements

### ValidationResult dataclass

- `is_valid` (bool) — Whether validation passed
- `errors` (list of str) — List of error messages (empty if valid)

### Function

`validate(data, schema)` — Validate a data dictionary against a schema dictionary. Return a `ValidationResult`.

### Schema format

The schema is a dict mapping field names to rule dicts:

```python
{
    "name": {"type": "str", "required": True, "min_length": 1, "max_length": 100},
    "age": {"type": "int", "min": 0, "max": 150},
    "email": {"type": "str", "pattern": ".*@.*"},
    "tags": {"type": "list", "items": {"type": "str"}},
}
```

### Supported types

`str`, `int`, `float`, `bool`, `list`, `dict`

### Supported rules

- `required` (bool) — Field must be present in data
- `type` (str) — Expected type name
- `min` (number) — Minimum value (for int, float)
- `max` (number) — Maximum value (for int, float)
- `min_length` (int) — Minimum length (for str, list)
- `max_length` (int) — Maximum length (for str, list)
- `pattern` (str) — Regex pattern the value must match (for str)
- `items` (dict) — Schema for each item in a list

## Rules

- Only modify files in the `setup/` directory
- Each validation error should produce a descriptive error message
- A missing non-required field should not produce errors
- Type checking should happen before other rule checks

## Examples

```python
schema = {"name": {"type": "str", "required": True, "min_length": 1}}
result = validate({"name": "Alice"}, schema)
# result.is_valid == True, result.errors == []

result = validate({}, schema)
# result.is_valid == False, result.errors contains a "required" error
```
