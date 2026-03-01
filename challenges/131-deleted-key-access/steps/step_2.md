# Step 2: Delete Expired Key

The `"temp_token"` in `setup/memory.json` has expired and must be removed.

Delete the `"temp_token"` key from the JSON object in `setup/memory.json`. The remaining keys (`"name"` and `"role"`) must be preserved with their original values.

After this step, `setup/memory.json` should look like:

```json
{
  "name": "Alice",
  "role": "admin"
}
```
