# Step 2: Compact Memory

Compact the memory stored in `setup/memory.json`.

**Rule:** Only keep keys whose numeric suffix is a **multiple of 100**. Remove all other entries.

The keys to keep are: `key_100`, `key_200`, `key_300`, `key_400`, `key_500`, `key_600`, `key_700`, `key_800`, `key_900`, `key_1000`.

After compaction, `setup/memory.json` should contain exactly 10 key-value pairs. All other entries must be removed.
