# Challenge 201: FD Exhaustion

## Difficulty: Hard
## Category: Failure Recovery

## Description

A log-analysis script (`setup/analyzer.py`) opens one file descriptor per log file and keeps them all open simultaneously while cross-referencing entries. With 50 log files in `setup/logs/`, this exhausts the file descriptor limit on constrained systems.

The crash report is in `setup/fd_crash.json`.

Your job:
1. Rewrite `setup/analyzer.py` so it processes log files one at a time (or in small batches), never holding more than 5 file descriptors open simultaneously.
2. The analyzer must read all 50 log files and produce `setup/analysis.json` containing:
   - `total_lines` (int): total number of log lines across all files
   - `error_count` (int): number of lines containing the word "ERROR"
   - `warning_count` (int): number of lines containing the word "WARNING"
   - `files_processed` (int): must be 50
   - `max_concurrent_fds` (int): must be <= 5
3. The rewritten analyzer must use context managers (`with` statements) properly and close files after reading.

## Expected Output

- `setup/analyzer.py` — rewritten to use bounded file descriptors
- `setup/analysis.json` — analysis results

## Scoring

Your solution is verified by `tests/verify.py`. All tests must pass.
