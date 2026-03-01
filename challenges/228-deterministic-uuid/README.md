# Challenge 228: Deterministic UUID

## Objective

Modify a UUID generator to produce deterministic, reproducible UUIDs from the same input.

## Context

Random UUIDs (uuid4) are non-deterministic — each call produces a different value. This breaks reproducibility in testing, caching, and idempotent operations. Deterministic UUIDs (uuid5) use a namespace and a name to always produce the same UUID for the same input, which is essential for reproducible systems.

## Task

Read `setup/generator.py` which contains a function that generates UUIDs for user records using `uuid.uuid4()` (random). Modify the file so that:

1. The `generate_id(name: str)` function produces a **deterministic** UUID for a given name input
2. Use `uuid.uuid5()` with the namespace `uuid.NAMESPACE_DNS` and the input name as the name argument
3. The function should still return a string representation of the UUID
4. Calling `generate_id("alice")` must always return the same UUID string, every time

Also modify the `generate_batch(names: list)` function so it returns a dictionary mapping each name to its deterministic UUID.

The file should remain a valid Python module that can be imported.

## Requirements

- Replace `uuid4()` with `uuid5(NAMESPACE_DNS, name)`
- Same input must always produce the same output
- `generate_id("alice")` must return a valid UUID string
- `generate_batch(["alice", "bob"])` must return `{"alice": "<uuid>", "bob": "<uuid>"}`
- Module must be importable without errors

## Verification

```bash
python3 tests/verify.py
```
