# Challenge 218: Sandbox Escape Prevention

## Objective

Harden a Python code sandbox that is supposed to restrict what user-submitted code can do, but currently has **gaps that allow escape** via subprocess calls, file I/O, and dangerous builtins.

## Setup

- `setup/sandbox.py` — A module with a `run_sandboxed(code_string)` function that executes user-supplied Python code in a restricted environment. The sandbox attempts to block dangerous operations but has several bypasses.

## What You Must Do

1. Open `setup/sandbox.py` and find the `run_sandboxed` function.
2. The current sandbox has these gaps:
   - **Gap 1**: It blocks `import os` but not `__import__('os')` or `importlib`.
   - **Gap 2**: It blocks `open()` in the text but not `builtins.open` or `io.open`.
   - **Gap 3**: It does not block `subprocess`, `sys`, or `shutil` imports.
   - **Gap 4**: It does not block `eval()` or `exec()` calls within the sandboxed code.
3. Fix the sandbox so that:
   - Safe operations work: arithmetic, string operations, list/dict manipulation, built-in functions like `len()`, `range()`, `sorted()`, `max()`, `min()`.
   - Dangerous operations are blocked: file I/O, subprocess, system commands, dynamic imports of blocked modules, eval/exec within sandbox.
4. The function should return `{"status": "ok", "result": ...}` for safe code and `{"status": "blocked", "message": "..."}` for blocked operations.

## Constraints

- Do NOT change the function signature.
- Safe built-in functions must remain available.
- The sandbox must use an allowlist approach for builtins, not a blocklist.
