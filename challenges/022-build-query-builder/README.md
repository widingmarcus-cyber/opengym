# Challenge 022: Build Query Builder

## Difficulty: Medium

## Task

The file `setup/query_builder.py` is empty. Implement a fluent SQL query builder with a `Query` class.

## Requirements

The `Query` class must support the following chainable methods:

1. `table(name)` — Set the table name
2. `select(*columns)` — Set the columns to select. If not called, default to `*`
3. `where(condition)` — Add a WHERE condition (multiple calls are ANDed together)
4. `order_by(column, direction="ASC")` — Add an ORDER BY clause
5. `limit(n)` — Set the LIMIT
6. `offset(n)` — Set the OFFSET
7. `build()` — Return the SQL query string

All methods except `build()` should return `self` for chaining.

## Rules

- Only modify files in the `setup/` directory
- `build()` should raise `ValueError` if no table has been set
- SQL keywords should be uppercase
- Clauses should appear in order: SELECT, FROM, WHERE, ORDER BY, LIMIT, OFFSET

## Examples

```python
q = Query().table("users").select("name", "email").where("age > 18").order_by("name").limit(10)
q.build()
# "SELECT name, email FROM users WHERE age > 18 ORDER BY name ASC LIMIT 10"

q = Query().table("products").where("price > 100").where("in_stock = 1").build()
# "SELECT * FROM products WHERE price > 100 AND in_stock = 1"
```
