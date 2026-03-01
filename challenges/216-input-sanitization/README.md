# Challenge 216: Input Sanitization

## Objective

Fix a CLI tool that is vulnerable to **SQL injection** and **command injection** due to unsanitized user inputs.

## Setup

- `setup/tool.py` — A module with two functions:
  - `query_user(db_path, username)` — Queries a SQLite database for a user by name. Currently uses string formatting (vulnerable to SQL injection).
  - `ping_host(hostname)` — Pings a host by constructing a shell command. Currently uses string concatenation with `os.system()` (vulnerable to command injection).

## What You Must Do

1. Fix `query_user` to use **parameterized queries** instead of string formatting.
2. Fix `ping_host` to use **subprocess with argument lists** instead of shell command strings, and validate the hostname input.
3. Both functions must still work correctly for legitimate inputs:
   - `query_user("users.db", "alice")` should return the user record.
   - `ping_host("localhost")` should return success.
4. Injection attempts must be blocked:
   - `query_user(db, "' OR 1=1 --")` must NOT return all users.
   - `ping_host("localhost; rm -rf /")` must NOT execute the injected command.

## Constraints

- Do NOT change function signatures.
- `query_user` must use SQLite parameterized queries (`?` placeholders).
- `ping_host` must NOT use `os.system()` or `shell=True`. Use `subprocess.run()` with a list of arguments.
- `ping_host` must validate that the hostname contains only alphanumeric characters, dots, hyphens, and colons.
