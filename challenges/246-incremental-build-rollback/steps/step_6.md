# Step 6: Build Manifest

Write a build manifest documenting the final state of the system.

## Requirements

Create `setup/build_manifest.json` with the following structure:

```json
{
  "module_versions": {
    "module_a": "v1",
    "module_b": "v5",
    "module_c": "v3"
  },
  "pipeline_result_sha256": "<SHA256 hex digest of the contents of setup/pipeline_result.json>",
  "modules": ["module_a", "module_b", "module_c"],
  "rollback_performed": true
}
```

## Details

- `module_versions`: The version identifiers for each module. Module A was built in session 1 (v1), module B was fixed in session 5 (v5), module C was built in session 3 (v3).
- `pipeline_result_sha256`: Compute the SHA256 hash of the raw file contents of `setup/pipeline_result.json`.
- `modules`: List of module names in order.
- `rollback_performed`: Must be `true` because module B was rolled back in session 5.
