# Step 3: Export Remaining Data

Read `setup/memory.json` and write all remaining key-value pairs to `setup/answer.json` as a flat JSON object (dict).

The output must contain only the keys that currently exist in memory.json. Do not include any keys that were previously deleted.

Example format:

```json
{
  "name": "Alice",
  "role": "admin"
}
```
