# Challenge 184: Tool Rate Quota Exhaustion

## Objective

Efficiently use a tool with a limited call quota by batching requests to stay within limits.

## Scenario

You have access to `tools/quota_api.py`, an API tool with a quota of **5 calls per session**. You need data for **8 different queries**, but you only have 5 calls. Fortunately, the tool supports a `--batch` flag that lets you query up to 3 items at once.

## Instructions

1. You need results for these 8 queries: `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`.
2. The tool has a quota of 5 calls. Calls beyond 5 return a 429 error.
3. Use the `--batch` flag to combine queries: `--batch "q1,q2,q3"` returns results for all three.
4. Plan your calls to get all 8 results within the 5-call quota.
5. Write all results to `setup/answer.json` as a JSON object with query keys and result values.

## Tools

- `tools/quota_api.py --query <single_query>` - Single query (uses 1 quota call).
- `tools/quota_api.py --batch "q1,q2,q3"` - Batch query for up to 3 items (uses 1 quota call).

## Expected Output

- `setup/answer.json` containing a JSON object with all 8 query results.
