# Challenge 100: The Gauntlet

**Difficulty:** Hard
**Category:** Multi-step
**Language:** Python

## Overview

This is the ultimate challenge. The Gauntlet combines multiple skills across 5 phases, each testing a different core competency. You must complete all phases to pass.

## Phases

### Phase 1: Fix
Debug a broken function in `setup/phase1_fix.py`. The `parse_records` function is supposed to parse pipe-delimited records into a list of dicts, and `filter_records` should perform case-insensitive filtering. Both have bugs that need to be found and fixed.

### Phase 2: Implement
Write a new function from scratch in `setup/phase2_implement.py`. The `summarize_records` function must group records by a specified field and count unique values of another field.

### Phase 3: Refactor
Clean up messy but functional code in `setup/phase3_refactor.py`. The `process_employees` function works correctly but has poor code quality. Refactor it so the logic is preserved while improving readability and eliminating repetitive patterns.

### Phase 4: Configure
Fix a broken YAML configuration in `setup/phase4_config.yaml`. The config has values that are the wrong type or invalid. Correct them so the configuration is valid and sensible.

### Phase 5: Integrate
Wire everything together in `setup/phase5_integrate.py`. The `run_pipeline` function must load config, parse records, optionally filter them, summarize the results, and return a structured output.

## Verification

```bash
pytest tests/ -v
```

All 12 tests must pass.
