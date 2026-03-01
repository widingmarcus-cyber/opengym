# Step 1: Ingest Raw Data

Read the file `setup/raw_data.txt`. It contains 1000 lines, each in the format:

```
key_001=value_001
key_002=value_002
...
key_1000=value_1000
```

Parse every line and store ALL 1000 key-value pairs in `setup/memory.json` as a single JSON object. For example:

```json
{
  "key_001": "value_001",
  "key_002": "value_002",
  ...
  "key_1000": "value_1000"
}
```

The resulting file must be valid JSON containing exactly 1000 keys.
