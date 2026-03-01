# Step 2: Returns, Leak Detection, and Rebalancing

## Task

Process resource returns, detect leaks, and produce the final pool state.

1. Read `setup/pool_state.json` (from Step 1) and `setup/return_events.json`.
2. Process each return event:
   - Mark the resource as "available" and clear allocation info.
   - Log the return.
3. After processing returns, detect leaks:
   - A leak is any resource still "in_use" whose `ttl_minutes` has expired (compare `allocated_at` + `ttl_minutes` against the current time "2024-01-15T12:00:00Z").
   - Forcefully reclaim leaked resources and mark them as "available".
4. Write `setup/return_log.json`, `setup/leak_report.json`, and `setup/final_pool_state.json`.

## Expected Output

`setup/return_log.json`:
```json
{
  "returns": [
    {
      "return_id": "<id>",
      "resource_id": "<id>",
      "returned_by": "<requester>",
      "status": "returned"
    },
    ...
  ]
}
```

`setup/leak_report.json`:
```json
{
  "check_time": "2024-01-15T12:00:00Z",
  "leaks_detected": <number>,
  "leaks": [
    {
      "resource_id": "<id>",
      "allocated_to": "<requester>",
      "allocated_at": "<timestamp>",
      "ttl_minutes": <ttl>,
      "expired_at": "<computed expiry>",
      "action": "reclaimed"
    },
    ...
  ]
}
```

`setup/final_pool_state.json`:
```json
{
  "total_resources": 10,
  "available": <count>,
  "in_use": <count>,
  "resources": [ ... ]
}
```
