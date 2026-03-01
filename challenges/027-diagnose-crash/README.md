# Challenge 027: Diagnose the Crash

## Difficulty: Easy

## Task

A data processing pipeline crashed in production. You have been given the crash log (`setup/crash_log.txt`) and the source code (`setup/app.py`).

Your job is to read the stack trace, identify the root cause, and fill in the diagnosis functions in `setup/diagnosis.py`.

## Files

```
setup/
  crash_log.txt       # The full stack trace and error log
  app.py              # The source code of the data processing pipeline
  diagnosis.py        # Stub file - fill in the four functions
```

## What to Do

Read the crash log and source code, then update the four functions in `setup/diagnosis.py`:

1. `get_error_type()` - Return the exact Python exception type (e.g., "AttributeError")
2. `get_root_cause_file()` - Return the filename where the root cause is (e.g., "app.py")
3. `get_root_cause_line()` - Return the line number where the root cause originates
4. `get_fix_description()` - Return a string describing the fix (must mention "raise" and "exception")

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures in `diagnosis.py`
- Your answers must be precise and match the actual error
