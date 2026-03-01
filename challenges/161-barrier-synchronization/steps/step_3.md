You are the Aggregator agent. Your task is to check that all workers have reached the barrier and then combine their results.

1. Read `setup/barrier.json`. Verify that both `worker_a` and `worker_b` are `true` (both ready).
2. Read `setup/results/worker_a.json` and `setup/results/worker_b.json`.
3. Sum their `result` values.
4. Write `setup/answer.json` with:
   - `"total"`: the computed sum of all worker results
   - `"all_ready"`: `true` only if both workers signaled ready in barrier.json, otherwise `false`
