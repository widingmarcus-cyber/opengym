# Challenge 246: Six-Session Incremental Build with Rollback

**Dimension:** Planning
**Category:** Long-horizon
**Difficulty:** Hard

## Objective

Build a data processing system incrementally across 6 sessions. Each session adds or modifies a module. One session requires rolling back a module to an earlier version. You must keep versioned copies of your work to enable rollback.

## System Specification

The system consists of 3 modules (see `setup/spec.json` for details):

- **module_a** (`setup/module_a.py`): `sort_records(records)` — sorts records by priority descending, then name ascending.
- **module_b** (`setup/module_b.py`): `filter_records(records, min_priority)` — filters records based on a priority threshold.
- **module_c** (`setup/module_c.py`): `summarize_records(records)` — produces a summary dict with count, avg_priority, and sorted names.

## Session Plan

1. **Session 1**: Implement module_a with sort_records. Save a versioned copy.
2. **Session 2**: Implement module_b with filter_records (using >=). Save a versioned copy.
3. **Session 3**: Implement module_c with summarize_records. Save a versioned copy.
4. **Session 4**: Create setup/pipeline.py integrating all modules. Run on test_data.json.
5. **Session 5**: REGRESSION — module_b must use strict greater-than (>) instead of >=. Rollback to session 2 version, fix it, re-run pipeline.
6. **Session 6**: Write a build manifest documenting module versions and rollback.

## Key Requirements

- Keep versioned copies of modules (e.g., `setup/module_a_v1.py`) so rollback is possible.
- The final pipeline uses strict greater-than for filtering (`priority > min_priority`).
- Test data is in `setup/test_data.json`.
- Pipeline output goes to `setup/pipeline_result.json`.
- Build manifest goes to `setup/build_manifest.json`.

## Constraints

- Only files matching `setup/*.py` and `setup/*.json` persist between sessions.
- Each session has a 120-second timeout.
