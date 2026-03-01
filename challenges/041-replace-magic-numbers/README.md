# Challenge 041: Replace Magic Numbers

## Difficulty: Easy

## Task

The file `setup/server.py` is a server configuration module riddled with hardcoded "magic numbers." Numeric literals like `65535`, `30`, `3`, `4096`, `8080`, and `100` appear directly in function bodies with no explanation of what they represent.

**Your job:** Replace every magic number with a well-named module-level constant, while keeping all functions working identically.

## Requirements

After refactoring, `setup/server.py` must have:

1. Named constants defined at **module level**, including at least:
   - `MAX_PORT` (65535)
   - `DEFAULT_TIMEOUT` (30)
   - `MAX_RETRIES` (3)
   - `BUFFER_SIZE` (4096)
   - `DEFAULT_PORT` (8080)
   - `MAX_CONNECTIONS` (100)

2. All functions must reference these constants instead of inline numeric literals.

3. All existing functions must still exist and produce the same results:
   - `validate_port(port)`
   - `create_config(host, port, timeout, retries)`
   - `allocate_buffer(count)`
   - `check_connections(current)`
   - `retry_request(func)`
   - `get_server_defaults()`

## Rules

- Only modify files in the `setup/` directory
- Every function must produce the exact same output as before
- Magic numbers must be replaced with named constants, not just assigned to local variables
