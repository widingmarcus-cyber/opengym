# Challenge 094: Reconstruct Corrupted File

## Difficulty: Hard

## Task

The `setup/chunks/` directory contains numbered chunk files that together form a complete file. Some chunks may be out of order and some have corrupted checksum lines. Implement `setup/reconstructor.py` to reassemble the file.

## Chunk Format

Each chunk file (`chunk_001.dat`, `chunk_002.dat`, etc.) has the following format:

```
CHUNK <number> CHECKSUM <md5hex>
<content lines...>
```

- The first line is a header with the chunk number and an MD5 hex digest.
- The checksum is the MD5 hash of all content lines joined together (everything after the first line, including newlines between them but not a trailing newline after the last line).
- Some chunks have an incorrect checksum value in their header (corrupted).

## Requirements

1. `reconstruct(chunks_dir, output_path) -> dict` -- Read all chunk files from `chunks_dir`, reassemble the file, and write the result to `output_path`. Return a dict with:

   - `"status"`: `"ok"` if reconstruction succeeded.
   - `"chunks_processed"` (int): Total number of chunks read.
   - `"chunks_repaired"` (int): Number of chunks whose checksum was wrong and had to be recalculated.

### Behavior

- Read all `chunk_*.dat` files from the directory.
- Sort chunks by their number (from the header line).
- Verify each chunk's checksum against its content.
- If a checksum is wrong, recalculate the correct checksum (this counts as a repair) and use the content as-is.
- Concatenate the content of all chunks in order (each chunk's content joined with newlines, chunks separated by newlines).
- Write the final concatenated content to `output_path`.

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.
