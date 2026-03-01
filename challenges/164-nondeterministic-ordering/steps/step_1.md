You are the Processor agent. Your task is to process tasks and produce deterministically sorted results.

1. Read `setup/tasks.json`. It contains 6 tasks in scrambled order. Each task has an `id` and `data` field.
2. Process all tasks (you can process them in any order).
3. Write results to `setup/results.json` as a JSON array, sorted by task `id` in ascending order.

Each result entry should include the original `id` and `data`, plus a `"processed": true` field.

Expected output in results.json:
```json
[
  {"id": 1, "data": "alpha", "processed": true},
  {"id": 2, "data": "beta", "processed": true},
  {"id": 3, "data": "gamma", "processed": true},
  {"id": 4, "data": "delta", "processed": true},
  {"id": 5, "data": "epsilon", "processed": true},
  {"id": 6, "data": "zeta", "processed": true}
]
```

The results MUST be sorted by `id` regardless of the order you processed them.
