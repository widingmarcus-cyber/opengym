# Challenge 138: Memory TTL Expiration

## Difficulty: Medium

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can correctly handle time-to-live (TTL) expiration logic across sessions. You will store cache entries with TTL values and timestamps, then in a later session identify and remove expired entries.

## How It Works

- **Step 1:** Store 5 cache entries in `setup/cache.json`. Each entry has a `key`, `value`, `ttl_seconds`, and `created_at` timestamp. Three entries have `ttl_seconds: 60` and two have `ttl_seconds: 3600`.
- **Step 2:** The current time is `2024-01-01T00:05:00Z` (5 minutes / 300 seconds after creation). Remove expired entries and write the remaining valid entries to `setup/active_cache.json`.

## Rules

- Only modify files in the `setup/` directory
- Entries are expired if `current_time - created_at > ttl_seconds`
- The file `setup/cache.json` persists between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps. Everything else in `setup/` may be deleted by the runner between steps.

## Scoring

You pass if `setup/active_cache.json` contains exactly the 2 non-expired entries (those with `ttl_seconds: 3600`), and the 3 expired entries (with `ttl_seconds: 60`) are absent.
