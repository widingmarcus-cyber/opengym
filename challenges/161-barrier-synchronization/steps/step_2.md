You are Worker B. Your task is to complete a computation and signal readiness at the barrier.

1. Read `setup/data/worker_b_input.json`. It contains an object with a `"values"` array of numbers.
2. Compute the **sum** of all numbers in the `"values"` array. This is your result.
3. Write your result to `setup/results/worker_b.json`:
   ```json
   {"done": true, "result": <your_computed_sum>}
   ```
4. Update `setup/barrier.json` to mark yourself as ready. You MUST preserve Worker A's entry:
   ```json
   {"worker_a": true, "worker_b": true}
   ```

IMPORTANT: Read the existing barrier.json first and add your entry without removing Worker A's.
