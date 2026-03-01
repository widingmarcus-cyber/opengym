# Step 3: Second Update and Report

Read `setup/state.json`. It currently contains the state after the first update.

Make the following changes:
1. Increment `count` from 1 to 2
2. Append the string `"banana"` to the `items` array

Write the updated state back to `setup/state.json`.

Then, write the final state to `setup/answer.json` as well. Both files should contain:

```json
{
  "initialized": true,
  "count": 2,
  "items": ["apple", "banana"]
}
```
