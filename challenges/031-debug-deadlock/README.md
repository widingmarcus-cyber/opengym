# Challenge 031: Debug the Deadlock

## Difficulty: Hard

## Task

A multi-threaded worker system hangs intermittently. Two worker classes each acquire two shared locks, but they acquire them in opposite order, causing a classic deadlock.

Your job is to fix the lock ordering so both workers acquire locks in the same order and the deadlock is eliminated.

## Files

```
setup/
  workers.py    # Two worker classes and a run_workers() function
```

## How It Should Work

- `WorkerA` transfers a value from `account_x` to `account_y` (requires both locks)
- `WorkerB` transfers a value from `account_y` to `account_x` (requires both locks)
- `run_workers()` starts both workers and returns the final account balances
- Both workers must complete without hanging

## The Problem

The workers acquire locks in opposite order, creating a deadlock condition:
- WorkerA: lock_x -> lock_y
- WorkerB: lock_y -> lock_x

When both workers run concurrently, they can each hold one lock and wait for the other forever.

## Rules

- Only modify files in the `setup/` directory
- Do not change function signatures
- Both workers must still use locks for thread safety
- Both workers must still perform their transfer operations
- `run_workers()` must return a dict with 'account_x' and 'account_y' balances
