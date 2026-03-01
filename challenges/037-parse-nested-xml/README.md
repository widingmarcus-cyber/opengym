# Challenge 037: Parse Nested XML

## Difficulty: Medium

## Task

Extract values from a deeply nested XML configuration file and flatten them into dot-notation keys. Implement the parser in `setup/xml_parser.py`.

## Requirements

Implement this function in `setup/xml_parser.py`:

1. `parse_config(filepath)` -- Parse an XML file and return a flat dictionary where nested elements are represented using dot-notation keys.

### Flattening Rules

- Nested elements become dot-separated keys: `<database><host>localhost</host></database>` becomes `{"database.host": "localhost"}`.
- Attributes are prefixed with `@`: `<server port="8080"/>` within `<app>` becomes `{"app.server.@port": "8080"}`.
- Only leaf elements (those with text content and no child elements) produce key-value entries.
- Attribute values are always stored as strings.
- Text content is stripped of leading/trailing whitespace.
- The root element is not included in the key path.

## Data Format

The file `setup/config.xml` is a realistic application configuration XML with 4+ levels of nesting, attributes, and various data types.

## Rules

- Only modify files in the `setup/` directory
- Use only Python standard library modules (xml.etree.ElementTree is recommended)
- Do not use lxml or other external libraries
