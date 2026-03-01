# Step 1: Store Versioned Entries

Write 3 versioned entries for the key `"config"` to `setup/memory.json`.

Each entry should have the following structure:

```json
{"key": "config", "version": 1, "value": "alpha"}
```

Store all three versions:

| Version | Value   |
|---------|---------|
| 1       | alpha   |
| 2       | beta    |
| 3       | gamma   |

The file must be valid JSON. You may use an array of objects, or any structure that preserves all three version-value pairs. Example:

```json
[
  {"key": "config", "version": 1, "value": "alpha"},
  {"key": "config", "version": 2, "value": "beta"},
  {"key": "config", "version": 3, "value": "gamma"}
]
```
