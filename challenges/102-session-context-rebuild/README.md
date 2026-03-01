# Challenge 102: Session Context Rebuild

## Difficulty: Medium

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether you can analyze code, persist your findings, and then use those findings in a later session to fix bugs. The key twist: between sessions, the process is killed and restarted, so you cannot rely on in-context memory. Your notes file is the only bridge between sessions.

## How It Works

- **Step 1:** Analyze `setup/buggy_app.py`, which contains exactly 3 bugs. Do NOT fix them. Instead, write a detailed bug report to `setup/notes.md` describing each bug, its location, and how to fix it.
- **Step 2:** Using your notes from `setup/notes.md`, fix all 3 bugs in `setup/buggy_app.py`.

## Rules

- Only modify files in the `setup/` directory
- In step 1, do NOT fix the bugs — only write the report
- In step 2, use your notes to guide the fixes
- Both `setup/notes.md` and `setup/buggy_app.py` persist between sessions

## The 3 Bugs

The code is an order processing module with three functions. Each function has exactly one bug:

1. **Off-by-one error** in `find_pairs()` — causes an IndexError
2. **Wrong variable name** in `calculate_bill()` — uses the wrong variable
3. **Missing return** in `format_receipt()` — returns None instead of a string

## Scoring

All 3 test cases must pass: `find_pairs`, `calculate_bill`, and `format_receipt` must produce correct output.
