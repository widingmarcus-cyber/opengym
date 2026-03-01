# Challenge 042: Convert Callbacks to Async

## Difficulty: Medium

## Task

The file `setup/pipeline.py` implements a data processing pipeline using deeply nested callback-style functions. Each step passes its result to a callback function rather than returning it directly.

**Your job:** Convert the callback-based functions into `async/await` coroutines while preserving the same processing logic and results.

## Requirements

After refactoring, `setup/pipeline.py` must have these **async** functions:

1. `async def fetch_data(url)` — Simulates fetching data from a URL. Returns a dict with `url`, `data` (list of numbers), and `status`.
2. `async def process_data(data)` — Filters, transforms, and aggregates the data. Returns a dict with `filtered`, `transformed`, `total`, and `count`.
3. `async def save_results(results)` — Simulates saving the processed results. Returns a dict with `saved`, `record_count`, and `timestamp`.
4. `async def run_pipeline(url)` — Orchestrates the full pipeline: fetch -> process -> save. Returns the final save confirmation dict.

The old callback-based functions (`fetch_data_cb`, `process_data_cb`, `save_results_cb`, `run_pipeline_cb`) may be removed or kept — only the async versions will be tested.

## Rules

- Only modify files in the `setup/` directory
- All async functions must be proper coroutines (use `async def`)
- The processing logic must produce the same numerical results as the callback versions
- `run_pipeline` must call `fetch_data`, `process_data`, and `save_results` in sequence
