# Step 1: Initialize the Store

Write the following initial state to `setup/store.json`:

```json
{"version": 1, "data": "initial"}
```

This represents version 1 of the data store. The file `setup/store.json` will persist to subsequent sessions.

Note: There is also a file `setup/pending_write.flag` present. This flag indicates a write operation is in progress elsewhere. For now, just create the store -- the flag is not relevant to this step.
