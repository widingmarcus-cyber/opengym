# Challenge 092: Merge Config Files

## Difficulty: Medium

## Task

The file `setup/config_merger.py` contains a stub. Implement a function that merges configuration from multiple files in JSON, YAML, and TOML formats.

## Requirements

1. `merge_configs(paths, precedence="last_wins") -> dict` -- Read and merge configuration from the list of file paths. Supported formats are determined by file extension: `.json`, `.yaml`/`.yml`, and `.toml`.

### Merge Rules

- **Deep merge**: Nested dictionaries are merged recursively, not replaced.
- **Lists**: Lists are replaced entirely (not appended).
- **Scalars**: Later values override earlier values (with `last_wins`) or earlier values are kept (with `first_wins`).
- **`precedence="last_wins"`**: Files later in the `paths` list take precedence for conflicting keys.
- **`precedence="first_wins"`**: Files earlier in the `paths` list take precedence for conflicting keys.

### Notes

- For YAML parsing, use the `yaml` module (PyYAML) if available, or implement simple YAML parsing.
- For TOML parsing, use the built-in `tomllib` module (Python 3.11+).
- For JSON parsing, use the built-in `json` module.

## Rules

- Only modify files in the `setup/` directory.

## Example

```python
# base.json: {"db": {"host": "localhost", "port": 5432}, "debug": false}
# override.yaml: {"db": {"port": 5433, "name": "mydb"}, "debug": true}
result = merge_configs(["base.json", "override.yaml"])
# {"db": {"host": "localhost", "port": 5433, "name": "mydb"}, "debug": true}
```
