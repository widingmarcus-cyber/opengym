# Challenge 059: Read the Schema

## Difficulty: Medium

## Task

Answer questions about a complex JSON Schema by reading and analyzing `setup/schema.json`. Implement the functions in `setup/answers.py`.

## Setup

`setup/schema.json` contains a JSON Schema with nested objects, arrays, enums, required fields, patterns, and `$ref` references.

## Requirements

Implement all functions in `setup/answers.py`:

1. `required_fields()` — Return a sorted list of all required field names at the top level of the schema (list of str)
2. `valid_status_values()` — Return a sorted list of valid values for the `status` field (list of str)
3. `max_items_in_tags()` — Return the `maxItems` constraint on the `tags` array (int)
4. `address_pattern()` — Return the `pattern` regex for the `zip_code` field inside the `address` object (str)
5. `is_field_required(field_path)` — Given a dot-separated field path (e.g., `"address.street"`), return whether the field is required in its parent object (bool)
6. `get_field_type(field_path)` — Given a dot-separated field path, return the JSON Schema type of that field (str). For `$ref` references, follow the ref and return the resolved type.

## Rules

- Only modify `setup/answers.py`
- Parse the JSON Schema file to derive answers
- For `$ref` fields, follow the reference to `$defs` to resolve the type
