# Challenge 249: Tool Schema Drift Across Retries

## Scenario

You need to query an API tool (`tools/api.py`) for 8 items listed in `setup/items.txt`. The tool's response format **changes between calls** -- the schema drifts as you make more requests.

## The Tool

Run the API tool with an item name as argument:

```bash
python3 tools/api.py <item_name>
```

The tool returns JSON to stdout. It may also print schema version information to stderr. The tool tracks its own call count internally.

## Schema Versions

The tool cycles through 3 different response schemas based on the cumulative call count. The mappings are documented in `setup/schema_map.json`:

- **v1** (calls 1-3): `{"name": str, "value": float, "in_stock": bool}`
- **v2** (calls 4-6): `{"item_name": str, "item_value": float, "available": bool, "unit": str}`
- **v3** (calls 7-8): `{"n": str, "v": float, "s": bool, "u": str, "deprecated": true}`

Check stderr output for `SCHEMA_VERSION` hints on calls 4+.

## Your Task

1. Read the list of items from `setup/items.txt`.
2. Query `tools/api.py` for each item (one call per item, in order).
3. Normalize all responses to the **unified output format**.
4. Write the results to `setup/output.json`.

## Unified Output Format

```json
[
  {
    "name": "laptop",
    "value": 999.99,
    "in_stock": true
  },
  ...
]
```

Every item must use exactly these three fields: `name` (string), `value` (float), `in_stock` (boolean). No extra fields from v2 or v3 schemas should be included.

## Notes

- Query items in the order they appear in `setup/items.txt`.
- The tool maintains call state in `tools/.state/api_calls.json` -- do not modify this file.
- Each call to the tool increments the call counter, even if the same item is queried again.
