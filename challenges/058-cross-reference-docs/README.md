# Challenge 058: Cross-Reference Docs

## Difficulty: Medium

## Task

Answer questions that require cross-referencing information from three separate documentation files. Implement the functions in `setup/answers.py`.

## Setup

Three documentation files are provided:
- `setup/api_spec.md` — API endpoint specifications
- `setup/database_schema.md` — Database table definitions
- `setup/deployment_guide.md` — Environment configuration and deployment info

## Requirements

Implement all functions in `setup/answers.py`:

1. `endpoint_that_writes_to_users()` — Which API endpoint writes to the users table? Return the endpoint path (str)
2. `env_var_for_database_host()` — What environment variable configures the database host? Return the variable name (str)
3. `tables_accessed_by_orders_endpoint()` — Which database tables are accessed by the `/api/orders` endpoint? Return a sorted list (list of str)
4. `port_for_production()` — What port does the application run on in production? Return as int
5. `endpoints_requiring_auth()` — Which endpoints require authentication? Return a sorted list of endpoint paths (list of str)
6. `max_connections_env_var()` — What environment variable controls the maximum database connections? Return the variable name (str)
7. `table_for_audit_logs()` — What table stores audit log entries? Return the table name (str)
8. `cache_ttl_for_products()` — What is the cache TTL (in seconds) for the products endpoint? Return as int

## Rules

- Only modify `setup/answers.py`
- Answers require reading and cross-referencing multiple documents
