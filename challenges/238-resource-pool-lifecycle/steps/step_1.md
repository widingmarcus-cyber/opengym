# Step 1: Allocate Resources

## Task

Process the allocation requests in `setup/allocation_requests.json` against the resource pool in `setup/resource_pool.json`.

1. Read the resource pool and allocation requests.
2. For each request (in order):
   - Find an available resource that meets the minimum CPU and memory requirements.
   - Use **best-fit** strategy: pick the resource with the smallest total capacity (CPU + memory) that still satisfies the requirements.
   - If no resource is available, mark the request as "denied".
   - If allocated, mark the resource as "in_use" and record the allocation.
3. Write `setup/allocation_log.json` with the result of each request.
4. Write `setup/pool_state.json` with the current state of all resources after processing all requests.

## Expected Output

`setup/allocation_log.json`:
```json
{
  "allocations": [
    {
      "request_id": "<id>",
      "requester": "<name>",
      "resource_id": "<allocated resource or null>",
      "status": "allocated" | "denied",
      "reason": "<reason if denied>"
    },
    ...
  ]
}
```

`setup/pool_state.json`:
```json
{
  "resources": [
    {
      "resource_id": "<id>",
      "cpu": <cores>,
      "memory_gb": <gb>,
      "status": "available" | "in_use",
      "allocated_to": "<requester or null>",
      "allocated_at": "<timestamp or null>",
      "ttl_minutes": <ttl or null>
    },
    ...
  ]
}
```
