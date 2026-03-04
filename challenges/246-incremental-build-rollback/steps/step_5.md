# Step 5: Regression Fix with Rollback

**REGRESSION DETECTED**: `module_b`'s filter is using the wrong comparison operator.

## Problem

The current `filter_records` uses `>=` (greater-than-or-equal), but the correct behavior should be **strict greater-than** (`>`). Records with priority exactly equal to `min_priority` should be **excluded**.

## Requirements

1. Revert `setup/module_b.py` to its session-2 version by copying from `setup/module_b_v2.py`
2. Fix the reverted code to use strict greater-than (`>`) instead of `>=`
3. Save the fixed version as `setup/module_b_v5.py`
4. Re-run the pipeline (from `setup/pipeline.py`) to update `setup/pipeline_result.json` with the corrected filtering

## Expected Impact

With `min_priority=3` and strict `>`:
- Records with priority **exactly 3** are now excluded
- Only records with priority **4, 5, 6, 7, etc.** are kept
