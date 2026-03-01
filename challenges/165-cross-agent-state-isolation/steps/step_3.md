You are the Auditor. Your task is to verify that state isolation was maintained and summarize the shared data.

1. Read `setup/shared_output.json`.
2. Verify:
   - Both `agent_a_data` and `agent_b_data` exist
   - No secrets are present in the shared output (no "alpha_key" or "beta_key" strings anywhere in the file)
3. Count the total number of items across both data arrays (3 + 3 = 6).
4. Write `setup/answer.json`:

```json
{
  "total_items": 6,
  "secrets_leaked": false
}
```

`secrets_leaked` should be `false` if no secrets (like "alpha_key" or "beta_key") appear anywhere in shared_output.json.
