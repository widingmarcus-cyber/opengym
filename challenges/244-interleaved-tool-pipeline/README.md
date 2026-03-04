# Challenge 244: Interleaved Multi-Tool Pipeline

**Dimension:** Tool-use
**Category:** Tool-orchestration
**Difficulty:** Hard

## Objective

Process 6 data items through a 4-tool pipeline with interleaved execution order and per-tool call budgets.

## Instructions

1. Read the pipeline specification from `setup/pipeline_spec.json`. It defines an exact 10-step sequence of tool calls and the budget (maximum number of invocations) for each tool.

2. Read the data items from `setup/data_items.json`. There are 6 items to process.

3. The tools are located in the `tools/` directory:
   - `tools/transform.py` — Transforms records (multiplies value by 2). Budget: 3 calls.
   - `tools/validate.py` — Validates records (checks values are positive). Budget: 3 calls.
   - `tools/enrich.py` — Enriches records with extra metadata. Budget: 2 calls.
   - `tools/emit.py` — Writes final records to output. Budget: 2 calls.

4. Each tool is a Python script that takes two arguments:
   - Arg 1: path to an input JSON file
   - Arg 2: path to an output JSON file

5. Tools track their own call counts in `tools/.state/` and will refuse to run if their budget is exceeded.

6. Execute the tools in the exact interleaved sequence defined in the pipeline spec. You must split and batch your data items across calls to stay within each tool's budget while processing all 6 items.

7. The final output must be written to `setup/output.json` (via the emit tool).

## Expected Output

`setup/output.json` must contain all 6 items, where each item:
- Has its `value` field doubled (original * 2)
- Has `"enriched": true`
- Has been validated

## Constraints

- You must not exceed any tool's call budget.
- You must invoke tools in the sequence specified in the pipeline spec.
- Tool state is tracked in `tools/.state/` — do not tamper with it.
