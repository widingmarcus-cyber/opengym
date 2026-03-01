You are Worker A. Your task is to complete a computation and signal readiness at the barrier.

1. Read `setup/data/worker_a_input.json`. It contains an object with a `"values"` array of numbers.
2. Compute the **sum** of all numbers in the `"values"` array. This is your result.
3. Write your result to `setup/results/worker_a.json`:
   ```json
   {"done": true, "result": <your_computed_sum>}
   ```
4. Create `setup/barrier.json` to mark yourself as ready:
   ```json
   {"worker_a": true}
   ```

Note: Since you are the first worker, you can create barrier.json fresh.
