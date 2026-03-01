# Step 4: Write the Final Configuration

This is the final step. Read ALL accumulated requirements from `setup/constraints.json`.

Write the complete server configuration to `setup/server_config.json`. It must satisfy ALL constraints from all previous sessions.

Use this exact format:

```json
{
  "port": 8443,
  "tls": {
    "enabled": true,
    "version": "1.3"
  },
  "rate_limit": {
    "requests_per_minute": 100,
    "burst": 20
  },
  "logging": {
    "stdout": {
      "level": "INFO"
    },
    "file": {
      "path": "/var/log/app.log",
      "level": "DEBUG"
    }
  }
}
```

Make sure every field is present and matches the requirements exactly.
