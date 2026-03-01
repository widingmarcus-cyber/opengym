# Challenge 044: Decompose the God Class

## Difficulty: Hard

## Task

The file `setup/app_manager.py` contains a single massive `AppManager` class with ~25 methods that handles everything: database operations, caching, validation, and formatting. This "God Class" violates the Single Responsibility Principle.

**Your job:** Decompose `AppManager` into four focused classes, then refactor `AppManager` to orchestrate them via composition.

## Requirements

After refactoring, `setup/app_manager.py` must contain (all in the **same file**):

1. **`DatabaseManager`** class with methods:
   - `connect(db_name)` — Connect to a database, returns connection info
   - `disconnect()` — Disconnect from the database
   - `query(table, conditions)` — Query records from a table
   - `insert(table, record)` — Insert a record into a table
   - `update(table, record_id, fields)` — Update a record
   - `delete(table, record_id)` — Delete a record
   - `count(table, conditions)` — Count records in a table
   - `table_exists(table)` — Check if a table exists

2. **`CacheManager`** class with methods:
   - `get_cache(key)` — Get a value from cache
   - `set_cache(key, value, ttl)` — Set a value in cache with TTL
   - `clear_cache()` — Clear all cache entries
   - `has_cache(key)` — Check if a key exists in cache
   - `get_cache_stats()` — Return cache hit/miss statistics

3. **`Validator`** class with methods:
   - `validate_user(data)` — Validate user data
   - `validate_order(data)` — Validate order data
   - `validate_email(email)` — Validate an email address
   - `validate_phone(phone)` — Validate a phone number
   - `validate_address(address)` — Validate an address dict
   - `validate_record(data, required_fields)` — Generic record validation

4. **`Formatter`** class with methods:
   - `format_report(title, data)` — Format data into a report string
   - `format_email(to, subject, body)` — Format an email message dict
   - `format_csv(headers, rows)` — Format data as CSV string
   - `format_json_response(data, status)` — Format a JSON API response
   - `format_log_entry(level, message)` — Format a log entry string
   - `format_table(headers, rows)` — Format data as a plain-text table

5. **`AppManager`** class — refactored to use composition:
   - Must have attributes: `db`, `cache`, `validator`, `formatter` (instances of the above)
   - Must still expose ALL original methods, delegating to the appropriate component
   - Serves as a facade over the four specialized classes

## Rules

- Only modify files in the `setup/` directory
- ALL classes must be in the same file (`setup/app_manager.py`)
- All original `AppManager` methods must still work with the same signatures and return values
- The four component classes must also work independently (not require `AppManager`)
