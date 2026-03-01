# Challenge 214: Env Secret Leak

## Objective

Audit and fix an application that **leaks environment secrets** (API keys, database passwords, tokens) into its log output and return values.

## Setup

- `setup/app.py` — An application module with functions that process configuration and log diagnostic information. Several functions inadvertently include secret environment variables in their output.

## What You Must Do

1. Open `setup/app.py` and identify every place where sensitive environment variables are leaked.
2. The following environment variables are considered secret and must NEVER appear in output:
   - `DATABASE_PASSWORD`
   - `API_SECRET_KEY`
   - `AWS_SECRET_ACCESS_KEY`
3. Fix the code so that:
   - Secret values are **redacted** (replaced with `"***"` or `"[REDACTED]"`) in all log output and return values.
   - Non-secret configuration values (like `APP_NAME`, `APP_ENV`, `DEBUG`) remain visible.
   - The application still functions correctly — it must still return configuration dicts and log messages, just with secrets masked.

## Constraints

- Do NOT change function signatures.
- Do NOT remove the logging or return statements — just redact the secret values.
- The redacted placeholder must be either `"***"` or `"[REDACTED]"`.
