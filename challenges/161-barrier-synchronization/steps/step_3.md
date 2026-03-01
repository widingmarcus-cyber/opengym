You are the Aggregator agent. Your task is to check that all workers have reached the barrier and then combine their results.

1. Read `setup/barrier.json`. Verify that both `worker_a` and `worker_b` are `true` (both ready).
2. Read `setup/results/worker_a.json` and `setup/results/worker_b.json`.
3. Sum their `result` values (42 + 58 = 100).
4. Write `setup/answer.json`:

```json
{
  "total": 100,
  "all_ready": true
}
```

`all_ready` should be `true` only if both workers signaled ready in barrier.json.
