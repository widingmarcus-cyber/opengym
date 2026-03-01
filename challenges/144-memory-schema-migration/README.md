# Challenge 144: Memory Schema Migration

## Difficulty: Hard

## Type: Multi-Session (2 steps)

## Dimension: Memory

## Overview

This challenge tests whether your agent can migrate persisted data from an old schema to a new schema, preserving existing values, renaming fields, and adding new fields with default values. This is a common real-world task when data formats evolve over time.

## How It Works

- **Step 1:** `setup/data.json` already contains records in an old schema. Migrate all records to a new schema: rename `name` to `full_name`, keep `age` unchanged, and add a new field `active` defaulting to `true`.
- **Step 2:** Read the migrated data and write the number of migrated records to `setup/answer.txt`.

## Rules

- Only modify files in the `setup/` directory
- The old schema has fields: `name` (string), `age` (number)
- The new schema has fields: `full_name` (string, renamed from `name`), `age` (number, unchanged), `active` (boolean, default `true`)
- The old `name` field must NOT exist in the migrated records
- The file `setup/data.json` persists between sessions

## What Gets Persisted Between Sessions

Only files listed in `metadata.yaml` under `persist` survive between steps.

## Scoring

You pass if:
- `setup/data.json` has 2 records, each with `full_name`, `age`, and `active` fields
- No record has a `name` field (old schema field must be removed)
- `setup/answer.txt` contains `2`
