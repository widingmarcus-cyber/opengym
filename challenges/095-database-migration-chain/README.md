# Challenge 095: Database Migration Chain

## Difficulty: Medium

## Task

Implement a series of database migrations using the provided `InMemoryDB` class, and a migration runner that executes them in order.

## Setup

- `setup/database.py` -- Provides the `InMemoryDB` class with methods for schema and data manipulation.
- `setup/migration_001.py` through `setup/migration_004.py` -- Stubs for each migration.
- `setup/migrate.py` -- Stub for the migration runner.

## Requirements

### Migrations

Each migration file must define a `run(db)` function that takes an `InMemoryDB` instance:

1. **migration_001.py**: Create a `users` table with columns `id` (int) and `name` (str).
2. **migration_002.py**: Add an `email` column (str) to the `users` table.
3. **migration_003.py**: Create an `orders` table with columns `id` (int), `user_id` (int), and `total` (float).
4. **migration_004.py**: Add a `status` column (str) to the `orders` table with a default value of `"pending"`.

### Migration Runner

`setup/migrate.py` must define `run_migrations(db)` that imports and runs all 4 migrations in order (001 through 004). It should return the db instance.

## InMemoryDB API

```python
db = InMemoryDB()
db.create_table(name, columns)        # columns: dict of {col_name: type}
db.add_column(table, col_name, col_type, default=None)
db.rename_column(table, old_name, new_name)
db.drop_column(table, col_name)
db.insert(table, row)                 # row: dict
db.query(table, filter_fn=None)       # returns list of dicts
db.get_schema(table)                  # returns dict of {col_name: type}
db.list_tables()                      # returns list of table names
```

## Rules

- Only modify files in the `setup/` directory.
- Use only the Python standard library.
