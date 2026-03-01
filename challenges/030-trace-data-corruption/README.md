# Challenge 030: Trace the Data Corruption

## Difficulty: Hard

## Task

A data pipeline produces corrupted output. The pipeline has 6 files and the corruption is subtle: data is correct after the first run but wrong on subsequent runs.

The bug involves shared mutable state being passed by reference and unexpectedly mutated somewhere in the pipeline.

## Project Structure

```
setup/
  app/
    __init__.py        # Package init
    config.py          # Default configuration dict
    loader.py          # Loads data using config
    transformer.py     # Transforms loaded data
    validator.py       # Validates transformed data
    reporter.py        # Generates final report
```

## How It Should Work

1. `config.py` holds a default config dict with processing parameters
2. `loader.py` loads raw data and applies config settings
3. `transformer.py` transforms data (scaling, filtering)
4. `validator.py` validates that data meets config thresholds
5. `reporter.py` generates a summary report

Each stage receives the config dict and uses its values. No stage should modify the config.

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- The pipeline must produce correct results on every run
- The default config in `config.py` must never be mutated by pipeline stages
