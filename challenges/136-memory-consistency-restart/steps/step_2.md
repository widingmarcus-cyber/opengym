# Step 2: First Update

Read `setup/state.json`. It currently contains the initialized state from the previous session.

Make the following changes:
1. Increment `count` from 0 to 1
2. Append the string `"apple"` to the `items` array

Write the updated state back to `setup/state.json`. After this step, the file should contain:

```json
{
  "initialized": true,
  "count": 1,
  "items": ["apple"]
}
```
