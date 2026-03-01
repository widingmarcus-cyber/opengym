# Challenge 229: Reproducible Build Hash

## Objective

Fix a build script so it produces identical output hashes when run multiple times with the same input.

## Context

Reproducible builds are critical for supply chain security, caching, and CI/CD. If building the same source code twice produces different artifacts, you cannot verify that a binary matches its source, and build caches become useless. Common sources of non-determinism include timestamps, random values, unordered data structures, and environment-dependent paths.

## Task

Read `setup/build.py` which simulates a build process. It reads source files from `setup/source/`, processes them, and writes a build manifest to `setup/build_output.json`. The manifest includes file contents, metadata, and a final hash.

**The problem**: Running `build.py` twice produces different hashes every time due to multiple sources of non-determinism. Fix all of them.

Sources of non-determinism to fix:

1. **Timestamp**: The build embeds the current timestamp. Replace with a fixed build epoch or remove it.
2. **Random build ID**: Uses `random.random()` for a build ID. Make it deterministic based on content.
3. **Unordered iteration**: Files are processed using `os.listdir()` which has no guaranteed order. Sort them.
4. **Environment leakage**: The build includes `os.getcwd()` in metadata. Remove or replace with a fixed value.

After fixing, running `python3 setup/build.py` twice in a row must produce an identical `setup/build_output.json` with the same hash.

## Requirements

- Fix ALL sources of non-determinism in `build.py`
- The script must still read all files from `setup/source/`
- The script must still produce `setup/build_output.json` with a `hash` field
- Running the script twice must produce byte-identical output
- Do NOT modify any files in `setup/source/`

## Verification

```bash
python3 tests/verify.py
```
